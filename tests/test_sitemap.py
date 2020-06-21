"""Tests sitemap functions."""

import contextlib

import enerator.sitemap


def test_sitemap_read_no_file(set_path):
    with contextlib.suppress(FileNotFoundError):
        (set_path / enerator.sitemap.SITEMAP).unlink()
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert isinstance(result, list)


def test_sitemap_read_file(set_path):
    payload = ["something", "else"]
    (set_path / enerator.sitemap.SITEMAP).write_text("\n".join(payload))
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_write_file(set_path):
    payload = ["value1", "value2"]
    enerator.sitemap.sitemap_write(payload)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert result == payload


def test_sitemap_add_new_file(set_path):
    module = "pages.mypage"
    enerator.sitemap.sitemap_add(module)

    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert module in result
