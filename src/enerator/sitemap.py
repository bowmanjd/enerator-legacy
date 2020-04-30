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


def sitemap_update(sitepath: pathlib.PurePosixPath, module: str, title: str) -> None:
    """Update sitemap file with page information.

    Args:
        sitepath: URL path for this page, as a pathlib PurePosixPath.
        module: string form of Python module name
        title: string to use as the title of the page

    """
    sitemap = sitemap_read()
    sitemap[module] = {
        "sitepath": str(sitepath),
        "title": title,
    }
    sitemap_write(sitemap)


def sitemap_write(sitemap: dict) -> None:
    """Write page information to sitemap file.

    Args:
        sitemap: dict of all pages and page info. Will overwrite existing.
    """
    with SITEMAP.open("w") as fp:
        json.dump(sitemap, fp, indent=2)
    sitemap_read.cache_clear()
