"""Sitemap json config file handling."""


import functools
import pathlib
import typing

SITEMAP = pathlib.Path("pages.txt")


@functools.lru_cache(maxsize=2)
def sitemap_read() -> list:
    """Load page information from sitemap file.

    Returns:
        A list of modules to include in site
    """
    try:
        with SITEMAP.open() as fp:
            sitemap = [line.strip() for line in fp if not line.startswith("#")]
    except FileNotFoundError:
        sitemap = []
    return sitemap


def sitemap_loader() -> typing.Callable:
    """Parse each module in sitemap for related info."""


def sitemap_add(module: str) -> None:
    """Update sitemap file with page information.

    Args:
        module: string form of Python module name
    """
    sitemap = sitemap_read()
    sitemap = sorted(sitemap + [module])
    sitemap_write(sitemap)


def sitemap_write(sitemap: list) -> None:
    """Write page information to sitemap file.

    Args:
        sitemap: list of all page modules. Will overwrite existing.
    """
    SITEMAP.write_text("\n".join(sitemap))
    sitemap_read.cache_clear()
