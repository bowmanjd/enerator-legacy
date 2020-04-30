"""Tests sitemap functions."""

import contextlib
import json

import enerator.sitemap

from .cheaters import set_path  # noqa:WPS300


def test_sitemap_read_no_file(tmp_path):
    set_path(tmp_path)
    with contextlib.suppress(FileNotFoundError):
        (tmp_path / enerator.sitemap.SITEMAP).unlink()
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert isinstance(result, dict)


def test_sitemap_read_file(tmp_path):
    set_path(tmp_path)
    payload = {"key": "value"}
    (tmp_path / enerator.sitemap.SITEMAP).write_text(json.dumps(payload))
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_write_file(tmp_path):
    set_path(tmp_path)
    payload = {"key2": "value2"}
    enerator.sitemap.sitemap_write(payload)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_update_new_file(tmp_path):
    set_path(tmp_path)
    sitepath = "/mypage"
    module = "pages.mypage"
    title = "My Page"
    enerator.sitemap.sitemap_update(sitepath, module, title)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result[module]["sitepath"] == sitepath
    assert result[module]["title"] == title
