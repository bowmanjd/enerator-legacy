"""Tests for enerator."""


import argparse
import importlib
import pathlib

import enerator.commands
import enerator.sitemap

from .cheaters import set_path  # noqa:WPS300


def test_cmdline_gen(tmp_path: pathlib.Path, capsys) -> None:
    set_path(tmp_path)
    args = argparse.Namespace(
        sitepath="/programming", module="pages.programming.home", sitemap=True,
    )
    enerator.commands.add(args)
    cmd_args = ["gen", "--module", args.module, "--out", "out"]
    enerator.commands.parse_args(cmd_args)
    captured = capsys.readouterr()
    generated_file = pathlib.Path("out/programming/index.html")
    assert args.sitepath in captured.out
    assert str(generated_file) in captured.out
    assert generated_file.exists()


def test_cmdline_add_pages(tmp_path) -> None:
    set_path(tmp_path)
    sitepath1 = "/"
    module1 = "sites.home"
    args = ["add", "-s", sitepath1, module1]
    enerator.commands.parse_args(args)
    sitepath2 = "/programming"
    module2 = "sites.programming"
    args = ["add", "--sitepath", sitepath2, module2]
    enerator.commands.parse_args(args)
    page = importlib.import_module(module1)
    page2 = importlib.import_module(module2)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert page.page({})  # type: ignore
    assert page2.page({})  # type: ignore
    assert result[module1]["sitepath"] == sitepath1
    assert result[module2]["sitepath"] == sitepath2


def test_cmdline_add_template(tmp_path) -> None:
    set_path(tmp_path)
    module1 = "templates.main"
    args = ["add", "-n", module1]
    enerator.commands.parse_args(args)
    page = importlib.import_module(module1)
    enerator.sitemap.sitemap_read.cache_clear()
    pages = enerator.sitemap.sitemap_read()
    assert page.page({})  # type: ignore
    assert pages.get(module1) is None


def test_main(capsys) -> None:
    enerator.commands.main()
    captured = capsys.readouterr()
    assert "usage" in captured.out
