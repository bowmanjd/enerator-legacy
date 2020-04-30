"""Tests for enerator."""

import importlib
import os
import pathlib
import sys

import enerator.add

from .cheaters import set_path  # noqa:WPS300

sys.path = ["", *sys.path]


def test_module_to_path() -> None:
    modpath = enerator.add.module_to_path("pages.mydir.mypage")
    cwd_len = len(pathlib.Path.cwd().parts)
    assert modpath.parts[cwd_len:] == ("pages", "mydir", "mypage")


def test_create_dirs(tmp_path: pathlib.Path) -> None:
    """Test create_dirs."""
    set_path(tmp_path)
    dirpath = tmp_path / "parent_dir" / "child_dir"
    enerator.add.create_dirs(dirpath)
    content = (dirpath / "__init__.py").read_text()
    assert "import enerator" in content
    assert (dirpath.parent / "__init__.py").exists()
    assert not (tmp_path / "__init__.py").exists()


def test_add(tmp_path: pathlib.Path) -> None:
    os.chdir(tmp_path)
    module = "pages.programming.home"
    enerator.add.add(
        sitepath=pathlib.PurePosixPath("/programming"),
        module=module,
        title="Programming",
    )
    page = importlib.import_module(module)
    assert page.page({})  # type: ignore
