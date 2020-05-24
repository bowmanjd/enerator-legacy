"""Preview generated site in browser."""

import mimetypes
import pathlib
import typing

import uvicorn  # type: ignore

from enerator.generate import generate_page, routes

PORT = 8080
STATIC_DIR = "/assets"


def static_body(path: str) -> typing.Optional[bytes]:
    """Check if static file and return blob if so.

    Args:
        path: path string

    Returns:
        bytes or None
    """
    body = None
    if path.startswith(STATIC_DIR):
        source_path = pathlib.Path(path[1:])
        if source_path.exists():
            body = source_path.read_bytes()
    return body


def page_body(path: str) -> typing.Optional[bytes]:
    """Check if path exists and return generated blob if so.

    Args:
        path: path string

    Returns:
        bytes or None
    """
    body: typing.Optional[bytes]
    try:
        body = generate_page(routes()[path], {"devmode": True}).encode()
    except KeyError:
        body = None
    return body


async def app(scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
    """ASGI app.

    Args:
        scope: environment dict returned by server
        receive: function that will yield a new event dictionary
        send: function that takes a new event dictionary
    """
    content_type = "text/html"
    body = None
    body = static_body(scope["path"])
    if body is None:
        body = page_body(scope["path"])

    if body:
        content_type = mimetypes.guess_type(str(scope["path"]))[0] or content_type
        status = 200
    else:
        status = 404
        body = f"Cannot find {scope['path']}".encode()

    await send(
        {
            "type": "http.response.start",
            "status": status,
            "headers": [[b"content-type", content_type.encode()]],
        }
    )
    await send({"type": "http.response.body", "body": body})


def preview_page(module: str) -> None:
    """Preview page content.

    Args:
        module: string form of Python module name
    """
    uvicorn.run("enerator.preview:app", host="127.0.0.1", port=PORT, log_level="info")
