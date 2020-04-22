"""Tests for enerator."""


import argparse
import importlib
import os
import pathlib
import sys

import enerator.commands
import enerator.sitemap

PATH = sys.path


def test_module_to_path() -> None:
    modpath = enerator.commands.module_to_path("pages.mydir.mypage")
    cwd_len = len(pathlib.Path.cwd().parts)
    assert modpath.parts[cwd_len:] == ("pages", "mydir", "mypage")


def test_create_dirs(tmp_path: pathlib.Path) -> None:
    """Test create_dirs."""
    os.chdir(tmp_path)
    dirpath = tmp_path / "parent_dir" / "child_dir"
    enerator.commands.create_dirs(dirpath)
    content = (dirpath / "__init__.py").read_text()
    assert "import enerator" in content
    assert (dirpath.parent / "__init__.py").exists()
    assert not (tmp_path / "__init__.py").exists()


def test_cmd_add(tmp_path) -> None:
    os.chdir(tmp_path)
    sys.path = ["", *PATH]
    module = "pages.programming.home"
    args = argparse.Namespace(
        sitepath="/programming", module=module, title="Programming",
    )
    enerator.commands.cmd_add(args)
    page = importlib.import_module(module)
    assert page.page()


def test_cmdline_add(tmp_path) -> None:
    os.chdir(tmp_path)
    sys.path = ["", *PATH]
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
    assert page.page()
    assert page2.page()
    assert result[sitepath1]["module"] == module1
    assert result[sitepath1]["title"] == title1
    assert result[sitepath2]["module"] == module2
    assert result[sitepath2]["title"] == title2


def test_main(capsys) -> None:
    enerator.commands.main()
    captured = capsys.readouterr()
    assert "usage" in captured.out
