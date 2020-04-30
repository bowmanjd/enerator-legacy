"""Simple Static Site Generator using Python."""

import importlib
import pathlib
import sys

from enerator.sitemap import sitemap_read


def generate_page(module: str, rel: dict) -> str:
    """Generate page content.

    Args:
        module: string form of Python module name
        rel: dict with related information

    Returns:
        generated page text
    """
    page = importlib.import_module(module)
    return page.page(rel)  # type: ignore


def generate(module: str, out: pathlib.Path) -> pathlib.Path:
    """Generate page.

    Args:
        module: string form of Python module name
        out: output directory for static site

    Returns:
        Full path to generated filename
    """
    sys.path = ["", *sys.path]

    sitemap = sitemap_read()
    rel = sitemap[module]
    output_dir = (out / rel["sitepath"][1:]).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "index.html"
    web_content = generate_page(module, rel)
    output_path.write_text(web_content)
    return output_path
