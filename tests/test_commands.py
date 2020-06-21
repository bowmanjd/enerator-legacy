"""Tests for enerator."""


import argparse
import importlib
import pathlib

import enerator.commands
import enerator.sitemap


def test_cmdline_gen(set_path, capsys) -> None:
    args = argparse.Namespace(sitepath="/programming", module="pages.programming.home")
    enerator.commands.add(args)
    cmd_args = ["gen", "--module", args.module, "--output", "out"]
    enerator.commands.parse_args(cmd_args)
    captured = capsys.readouterr()
    generated_file = pathlib.Path("out/programming/index.html")
    assert args.sitepath in captured.out
    assert str(generated_file) in captured.out
    assert generated_file.exists()


def test_cmdline_add_pages(set_path) -> None:
    sitepath1 = "/"
    module1 = "sites.home"
    args = ["add", "-s", sitepath1, module1]
    enerator.sitemap.sitemap_read.cache_clear()
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
    assert module1 in result
    assert module2 in result
    assert page.CONFIG["path"] == sitepath1  # type: ignore
    assert page2.CONFIG["path"] == sitepath2  # type: ignore


def test_cmdline_add_template(set_path) -> None:
    module1 = "templates.main"
    args = ["add", module1]
    enerator.commands.parse_args(args)
    page = importlib.import_module(module1)
    enerator.sitemap.sitemap_read.cache_clear()
    pages = enerator.sitemap.sitemap_read()
    assert page.page({})  # type: ignore
    assert module1 not in pages


def test_main(capsys) -> None:
    enerator.commands.main()
    captured = capsys.readouterr()
    assert "usage" in captured.out
