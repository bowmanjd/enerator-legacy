"""Tests for enerator."""

import importlib
import pathlib

import enerator.add


def test_module_to_path() -> None:
    modpath = enerator.add.module_to_path("pages.mydir.mypage")
    cwd_len = len(pathlib.Path.cwd().parts)
    assert modpath.parts[cwd_len:] == ("pages", "mydir", "mypage")


def test_create_dirs(set_path) -> None:
    """Test create_dirs."""
    dirpath = set_path / "parent_dir" / "child_dir"
    enerator.add.create_dirs(dirpath)
    assert (dirpath.parent / "__init__.py").exists()
    assert not (set_path / "__init__.py").exists()


def test_add(set_path) -> None:
    module = "pages.programming.home"
    enerator.add.add(
        module=module, sitepath=pathlib.PurePosixPath("/programming"),
    )
    page = importlib.import_module(module)
    assert page.page({})  # type: ignore
