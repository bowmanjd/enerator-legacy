"""Preview generated site in browser."""

import asyncio
import mimetypes
import pathlib
import typing

import uvicorn  # type: ignore

from enerator.add import module_to_path
from enerator.generate import generate_page, load_module, routes

CHUNK_SIZE = 1024
MEG = 1048576
PORT = 8080
STATIC_DIR = "/assets"


class Response(typing.NamedTuple):
    """Response tuple."""

    body_gen: typing.AsyncGenerator
    status: int
    headers: list = [(b"content-type", b"text/html")]


async def not_found(scope: dict) -> Response:
    """Respond with 404.

    Args:
        scope: ASGI scope dict

    Returns:
        404 Response info and generator
    """  # noqa:DAR301
    status = 404

    async def body_gen() -> typing.AsyncGenerator[bytes, None]:
        yield f"{scope['path']} not found".encode()

    return Response(body_gen(), status)


async def static_body(scope: dict) -> Response:
    """Check if static file and return blob if so.

    Args:
        scope: ASGI scope dict

    Returns:
        response
    """  # noqa:DAR301
    source_path = pathlib.Path(scope["path"][1:])
    if source_path.exists():
        status = 200

        async def body_gen() -> typing.AsyncGenerator[bytes, None]:
            with source_path.open("rb") as fp:
                for chunk in iter(fp.read, b""):
                    yield chunk

        response = Response(
            body_gen(),
            status,
            [
                (
                    b"content-type",
                    (
                        mimetypes.guess_type(str(source_path))[0] or "text/plain"
                    ).encode(),
                )
            ],
        )
    else:
        response = await not_found(scope)
    return response


async def page_body_gen(module: str) -> typing.AsyncGenerator[bytes, None]:
    """Asynchronously yield page body.

    Args:
        module: module string

    Yields:
        Body of generated page, in bytes
    """
    body = generate_page(module, {"devmode": True}).replace(
        "</html>",
        "\n".join(
            (
                "<script>",
                f"  let eventSource = new EventSource('/sse/{module}');",
                "  eventSource.addEventListener('message', (e) => {",
                "    if (e.data === 'modified') {",
                "      window.location.reload();",
                "    }",
                "  });",
                "</script>",
                "</html>",
            )
        ),
    )
    yield body.encode()


async def page_body(scope: dict) -> Response:
    """Check if path exists and return generated blob if so.

    Args:
        scope: ASGI scope dict

    Returns:
        response
    """
    module = routes().get(scope["path"], "")
    if module:
        status = 200

        response = Response(page_body_gen(module), status)
    else:
        response = await not_found(scope)
    return response


def last_modified_times(files: list) -> dict:
    """Check last modified on all files in list.

    Args:
        files: list of file paths

    Returns:
        dict of files and timestamps
    """
    return {filepath: filepath.stat().st_mtime for filepath in files}


async def sse_body_gen(  # noqa:WPS210
    module: str, tls: bool
) -> typing.AsyncGenerator[bytes, None]:
    """Asynchronously yield event stream.

    Args:
        module: module string
        tls: using https?

    Yields:
        bytestream in a format to be consumed by EventSource
    """
    first_iteration = True
    rel, _ = load_module(module)
    watchlist = rel.get("watch", [])
    modpath = module_to_path(module)
    paths = [modpath.joinpath(path) for path in watchlist]
    modified = last_modified_times(paths)
    while True:
        changed = last_modified_times(paths)
        if changed != modified:
            modified = changed
            if first_iteration and not tls:
                yield f": {'.' * 2 * MEG}\n\n".encode()
                first_iteration = False
            yield "data: modified\n\n".encode()
        await asyncio.sleep(2)


async def sse(scope: dict) -> Response:
    """Stream events.

    Args:
        scope: ASGI scope dict

    Returns:
        response
    """  # noqa:DAR301
    status = 200
    tls = scope["scheme"] == "https"
    module = scope["path"].split("/", 2)[2]

    return Response(
        sse_body_gen(module, tls),
        status,
        [
            (b"content-type", b"text/event-stream"),
            (b"cache-control", b"no-cache"),
            (b"connection", b"keep-alive"),
        ],
    )


ROUTES = {
    "assets": static_body,
    "sse": sse,
}


async def app(scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
    """ASGI app.

    Args:
        scope: environment dict returned by server
        receive: function that will yield a new event dictionary
        send: function that takes a new event dictionary
    """
    route_key = scope["path"].split("/", 2)[1]
    response = await ROUTES.get(route_key, page_body)(scope)

    await send(
        {
            "type": "http.response.start",
            "status": response.status,
            "headers": response.headers,
        }
    )
    async for chunk in response.body_gen:
        await send({"type": "http.response.body", "body": chunk, "more_body": True})

    await send({"type": "http.response.body", "body": b""})


def preview_page() -> uvicorn.Server:
    """Preview page content.

    Returns:
        Uvicorn server (call run() method)
    """
    config = uvicorn.Config(
        "enerator.preview:app",
        host="0.0.0.0",
        lifespan="off",
        log_level="info",
        port=PORT,
        ssl_certfile="/home/jbowman/devel/localdev.bowmanjd.com+4.pem",
        ssl_keyfile="/home/jbowman/devel/localdev.bowmanjd.com+4-key.pem",
    )
    return uvicorn.Server(config=config)
