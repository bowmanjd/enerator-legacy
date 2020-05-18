"""Tests sitemap functions."""

import contextlib

import enerator.sitemap

from .cheaters import set_path  # noqa:WPS300


def test_sitemap_read_no_file(tmp_path):
    set_path(tmp_path)
    with contextlib.suppress(FileNotFoundError):
        (tmp_path / enerator.sitemap.SITEMAP).unlink()
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert isinstance(result, list)


def test_sitemap_read_file(tmp_path):
    set_path(tmp_path)
    payload = ["something", "else"]
    (tmp_path / enerator.sitemap.SITEMAP).write_text("\n".join(payload))
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_write_file(tmp_path):
    set_path(tmp_path)
    payload = ["value1", "value2"]
    enerator.sitemap.sitemap_write(payload)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_add_new_file(tmp_path):
    set_path(tmp_path)
    module = "pages.mypage"
    enerator.sitemap.sitemap_add(module)

    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert module in result
