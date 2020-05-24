"""Methods for creating/scaffolding pages."""

import pathlib
import typing

from enerator.sitemap import sitemap_add

INIT = '''#!/usr/bin/env python3
"""Page generator."""

import enerator

CONFIG = {{"title": "The tech blog of Jonathan Bowman", "path": "{sitepath}"}}


def page(rel: dict) -> str:
    """Output page content.

    Args:
        rel: related info (variables, etc.) as a dict

    Returns:
        string with page content
    """
    config = {{**CONFIG, **rel}}
    md = "*Hello*, {{title}}!"
    return enerator.md_highlight_and_parse(md)


if __name__ == "__main__":
    print(page({{}}))
'''


def add(module: str, sitepath: typing.Optional[pathlib.PurePosixPath]) -> pathlib.Path:
    """Add a page.

    This creates the designated directories and files and updates the
    sitemap.

    Args:
        module: string form of Python module name
        sitepath: desired URL path

    Returns:
        the path to the directory of the module
    """
    dirpath = module_to_path(module)
    mod_init = create_dirs(dirpath)
    if not mod_init.exists() or mod_init.stat().st_size == 0:
        mod_init.touch(0o775)  # noqa:WPS432
        mod_init.write_text(INIT.format(sitepath=sitepath))
    if sitepath is not None:
        sitemap_add(module)
    return dirpath


def create_dirs(dirpath: pathlib.Path) -> pathlib.Path:
    """Create directories and populate with appropriate __init__.py.

    Args:
        dirpath: a pathlib Path.

    Returns:
        path to __init__.py

    """
    cwd = pathlib.Path.cwd()
    mod_init = dirpath / "__init__.py"
    dirpath.mkdir(parents=True, exist_ok=True)
    for directory in mod_init.parents:
        if directory == cwd:
            break
        (directory / "__init__.py").touch()
    return mod_init


def module_to_path(module: str) -> pathlib.Path:
    """Convert module name to filesystem path.

    Args:
        module: string form of Python module name

    Returns:
        a pathlib Path for the directory structure corresponding
        to the module name
    """
    return pathlib.Path(module.replace(".", "/")).resolve()
