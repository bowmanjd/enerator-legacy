"""Helpers useful for any tests."""

import contextlib
import multiprocessing
import os
import pathlib
import ssl
import sys
import typing
import urllib.request

import pytest  # type:ignore

import enerator.add
import enerator.commands
import enerator.sitemap

PAGES = {
    "{prefix}.home": "/",
    "{prefix}.programming.home": "/programming",
    "{prefix}.personal.shopping": "/mystuff/shoppinglist",
}


@pytest.fixture(scope="function")
def set_path(tmp_path: pathlib.Path) -> typing.Generator:
    """Change to temp directory and adjust path.

    Args:
        tmp_path: pytest tmp_path fixture return new temp path

    Yields:
        new temp path
    """
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(old_cwd)
    enerator.sitemap.sitemap_read.cache_clear()


@pytest.fixture
def make_pages(request, set_path) -> typing.Generator:  # noqa:WPS210,WPS442
    """Create dummy pages.

    Args:
        request: context of calling test
        set_path: pytest tmp_path fixture return new temp path

    Yields:
        dict of newly created modules
    """
    new_pages = {}
    prefix = request.function.__name__
    for modtpl, sitepath in PAGES.items():
        module = modtpl.format(prefix=prefix)
        new_pages[module] = sitepath
        enerator.add.add(
            module=module, sitepath=pathlib.PurePosixPath(sitepath),
        )
    yield new_pages
    for modname in new_pages:
        with contextlib.suppress(KeyError):
            del sys.modules[modname]  # noqa:WPS420


@pytest.fixture
def http() -> typing.Callable:  # noqa:WPS210,WPS442
    ctxt = ssl.SSLContext()
    ctxt.load_cert_chain(
        "/home/jbowman/devel/localdev.bowmanjd.com+4.pem",
        keyfile="/home/jbowman/devel/localdev.bowmanjd.com+4-key.pem",
    )

    def req(urlpath: str):
        url = f"https://localhost:8080{urlpath}"
        return urllib.request.urlopen(url, context=ctxt)  # noqa:S310

    return req


@pytest.fixture
def server() -> typing.Generator:  # noqa:WPS210,WPS442
    proc = multiprocessing.Process(
        target=enerator.commands.parse_args, args=(("preview",),), daemon=True
    )
    proc.start()
    proc.join(0.25)
    yield proc
    proc.kill()
