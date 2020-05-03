"""Sitemap json config file handling."""


import functools
import json
import pathlib
import typing

SITEMAP = pathlib.Path("pages.json")


@functools.lru_cache(maxsize=2)
def sitemap_read() -> dict:
    """Load page information from sitemap file.

    Returns:
        A dict with sitemap information. This includes all pages,
        keyed by URL path.
    """
    try:
        with SITEMAP.open() as fp:
            sitemap = json.load(fp)
    except FileNotFoundError:
        sitemap = {}
    return sitemap


def sitemap_loader() -> typing.Callable:
    """Parse each module in sitemap for related info."""


def sitemap_update(module: str, page_info: typing.Mapping[str, str]) -> None:
    """Update sitemap file with page information.

    Args:
        module: string form of Python module name
        page_info: mapping of keys and values to update

    """
    sitemap = sitemap_read()
    existing = sitemap.get(module, {})
    sitemap[module] = {**existing, **page_info}
    sitemap_write(sitemap)


def sitemap_write(sitemap: dict) -> None:
    """Write page information to sitemap file.

    Args:
        sitemap: dict of all pages and page info. Will overwrite existing.
    """
    with SITEMAP.open("w") as fp:
        json.dump(sitemap, fp, indent=2)
    sitemap_read.cache_clear()
