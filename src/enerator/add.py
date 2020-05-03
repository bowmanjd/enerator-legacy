"""Methods for creating/scaffolding pages."""

import pathlib

from enerator.sitemap import sitemap_update

INIT = '''#!/usr/bin/env python3
"""Page generator."""

import enerator  # type: ignore

CONFIG = {
  "title": "Title of this page",
}


def page(rel: dict) -> str:
    """Output page content.

    Args:
        rel: related info (variables, etc.) as a dict

    Returns:
        string with page content
    """

    config = {**CONFIG, **rel}
    tpl = "<html><body><h1>{title}</h1>{body}</body></html>"
    md = "*Hello*, {title}!"
    config["body"] = enerator.md_highlight_and_parse(md)
    return tpl.format(**config)


if __name__ == "__main__":
    print(page(CONFIG))
'''


def add(
    module: str, sitepath: pathlib.PurePosixPath, sitemap: bool = True
) -> pathlib.Path:
    """Add a page.

    This creates the designated directories and files and updates the
    sitemap.

    Args:
        module: string form of Python module name
        sitepath: desired URL path
        sitemap: whether or not to add to sitemap

    Returns:
        the path to the directory of the module
    """
    dirpath = module_to_path(module)
    create_dirs(dirpath)
    if sitemap:
        sitemap_update(module, {"sitepath": str(sitepath)})
    return dirpath


def create_dirs(dirpath: pathlib.Path) -> None:
    """Create directories and populate with appropriate __init__.py.

    Args:
        dirpath: a pathlib Path.

    """
    cwd = pathlib.Path.cwd()
    mod_init = dirpath / "__init__.py"
    dirpath.mkdir(parents=True, exist_ok=True)
    if not mod_init.exists():
        mod_init.touch(0o775)  # noqa:WPS432
        mod_init.write_text(INIT)
    for directory in dirpath.parents:
        if directory == cwd:
            break
        (directory / "__init__.py").touch()


def module_to_path(module: str) -> pathlib.Path:
    """Convert module name to filesystem path.

    Args:
        module: string form of Python module name

    Returns:
        a pathlib Path for the directory structure corresponding
        to the module name
    """
    return pathlib.Path(module.replace(".", "/")).resolve()
