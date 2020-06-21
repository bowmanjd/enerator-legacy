"""Tests for enerator."""

import multiprocessing
import pathlib

from starlette.testclient import TestClient

import enerator.commands
import enerator.preview

HTTP_OK = 200
HTTP_NOT_FOUND = 404


def test_preview_app(make_pages: dict) -> None:
    client = TestClient(enerator.preview.app)  # type:ignore
    for urlpath in make_pages.values():
        assert client.get(urlpath).status_code == HTTP_OK


def test_preview_app_404(make_pages: dict) -> None:
    client = TestClient(enerator.preview.app)  # type:ignore
    assert client.get("/someridiculouspath").status_code == HTTP_NOT_FOUND


def test_preview_app_css(make_pages: dict) -> None:
    cssfile = pathlib.Path("assets/style.css")
    cssfile.parent.mkdir()
    cssfile.write_text("body {color: black;}")
    client = TestClient(enerator.preview.app)  # type:ignore
    assert client.get(str(cssfile)).status_code == HTTP_OK


def test_preview_page(make_pages: dict, http) -> None:
    server = enerator.preview.preview_page()
    proc = multiprocessing.Process(target=server.run, args=(), daemon=True)
    proc.start()
    proc.join(0.5)
    for urlpath in make_pages.values():
        with http(urlpath) as handle:
            assert handle.getcode() == HTTP_OK
            assert handle.read()
    proc.terminate()


def test_preview_cmd(make_pages: dict, http) -> None:
    proc = multiprocessing.Process(
        target=enerator.commands.parse_args, args=(("preview",),), daemon=True
    )
    proc.start()
    proc.join(0.5)
    for urlpath in make_pages.values():
        with http(urlpath) as handle:
            assert handle.getcode() == HTTP_OK
            assert handle.read()
    proc.terminate()
