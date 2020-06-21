"""Simple Static Site Generator using Python."""

import functools
import importlib
import pathlib
import sys
import typing

from enerator.add import module_to_path
from enerator.sitemap import sitemap_read

sys.path = list(dict.fromkeys(("", *sys.path)))


def link_name(module: str) -> str:
    """Convert module name to case with prefix.

    Args:
        module: module string

    Returns:
        Snake cased string with 'url' prefix
    """
    return f"url_{module.replace('.', '_')}"


@functools.lru_cache(maxsize=2)
def all_urls() -> dict:
    """Generate all links to all pages in sitemap.

    Returns:
        A dict of all page urls
    """
    return {link_name(module): url_for(module) for module in sitemap_read()}


def load_module(
    module: str, devmode: bool = False
) -> typing.Tuple[dict, typing.Callable]:
    """Load specific page generation module.

    Args:
        module: string form of Python module name
        devmode: live reload if True

    Returns:
        the loaded module
    """
    page = None
    if devmode:
        page = sys.modules.get(module)
        if page:
            importlib.reload(page)
    page = page or importlib.import_module(module)
    config = page.CONFIG  # type: ignore
    page_gen = page.page  # type: ignore
    return (config, page_gen)


def url_for(module: str) -> str:
    """Generate link to page.

    Args:
        module: module string

    Returns:
        Absolute path
    """
    rel, _ = load_module(module)
    return rel["path"]


@functools.lru_cache(maxsize=2)
def routes() -> dict:
    """Generate all links to all pages in sitemap.

    Returns:
        A dict of all page urls
    """
    return {url_for(module): module for module in sitemap_read()}


def generate_page(module: str, rel: dict) -> str:
    """Generate page content.

    Args:
        module: string form of Python module name
        rel: dict with related information

    Returns:
        generated page text
    """
    rel["modpath"] = module_to_path(module)
    rel = {**rel, **all_urls()}
    _, page = load_module(module, rel.get("devmode", False))
    return page(rel)


def generate(module: str, out: pathlib.Path) -> pathlib.Path:
    """Generate page.

    Args:
        module: string form of Python module name
        out: output directory for static site

    Returns:
        Full path to generated filename
    """
    rel, page = load_module(module)
    output_dir = (out / rel["path"][1:]).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    web_content = generate_page(module, rel)
    output_path.write_text(web_content)
    return output_path
