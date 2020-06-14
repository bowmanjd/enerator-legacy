"""Simple Static Site Generator using Python."""

import functools
import importlib
import pathlib
import sys
import typing

from enerator.add import module_to_path
from enerator.sitemap import sitemap_read

sys.path = list(dict.fromkeys(("", *sys.path)))

REMEMBER_PAGE_MODULES = 100


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


@functools.lru_cache(maxsize=REMEMBER_PAGE_MODULES)
def load_module(module: str) -> typing.Tuple[dict, typing.Callable]:
    """Load specific page generation module.

    Args:
        module: string form of Python module name

    Returns:
        the loaded module
    """
    page = importlib.import_module(module)
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
    _, page = load_module(module)
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
