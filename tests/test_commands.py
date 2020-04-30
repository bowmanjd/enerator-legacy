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
        sitepath="/programming", module="pages.programming.home", title="Programming",
    )
    enerator.commands.add(args)
    cmd_args = ["gen", "--module", args.module, "--out", "out"]
    enerator.commands.parse_args(cmd_args)
    captured = capsys.readouterr()
    generated_file = pathlib.Path("out/programming/index.html")
    assert args.sitepath in captured.out
    assert str(generated_file) in captured.out
    assert generated_file.exists()


def test_cmdline_add(tmp_path) -> None:
    set_path(tmp_path)
    sitepath1 = "/"
    module1 = "sites.home"
    title1 = "Jonathan Bowman"
    args = ["add", "-m", module1, "-t", title1, sitepath1]
    enerator.commands.parse_args(args)
    sitepath2 = "/programming"
    module2 = "sites.programming"
    title2 = "Jonathan Bowman's Programming"
    args = ["add", "--module", module2, "--title", title2, sitepath2]
    enerator.commands.parse_args(args)
    page = importlib.import_module(module1)
    page2 = importlib.import_module(module2)
    enerator.sitemap.sitemap_read.cache_clear()
    result = enerator.sitemap.sitemap_read()
    assert page.page({})  # type: ignore
    assert page2.page({})  # type: ignore
    assert result[module1]["sitepath"] == sitepath1
    assert result[module1]["title"] == title1
    assert result[module2]["sitepath"] == sitepath2
    assert result[module2]["title"] == title2


def test_main(capsys) -> None:
    enerator.commands.main()
    captured = capsys.readouterr()
    assert "usage" in captured.out
