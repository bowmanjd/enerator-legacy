"""Simple Static Site Generator using Python."""


from enerator.generate import load_module
from enerator.sitemap import sitemap_read


def url_for(module: str) -> str:
    """Generate link to page.

    Args:
        module: module string

    Returns:
        Absolute path
    """
    rel, _ = load_module(module)
    return rel["path"]


def all_urls() -> dict:
    """Generate all links to all pages in sitemap.

    Returns:
        A dict of all page urls
    """
    return {module: url_for(module) for module in sitemap_read()}
