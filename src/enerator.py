#!/usr/bin/env python3
"""Simple Static Site Generator using Python."""


import argparse
import functools
import json
import pathlib
import re
import sys

import cmarkgfm
import pygments
import pygments.formatters
import pygments.lexers

BRACE_RE = re.compile(r"{([^}]+)}")
CODE_RE = re.compile(r"^```([a-z]+)?$(.+?)^```$", re.S | re.M)
CMARK_FLAGS = 132096  # UNSAFE = 1 << 17; SMART = 1 << 10; CMARK_FLAGS = UNSAFE | SMART
FORMATTER = pygments.formatters.HtmlFormatter()
INIT = '''#!/usr/bin/env python3
"""Page generator"""

import enerator

def page():
    """Outputs page content."""
    content = """Hello, site content!"""
    return content

if __name__ == "__main__":
    page()
'''
SITEMAP = pathlib.Path("pages.json")


def create_dirs(dirpath):
    """Create directories and populate with appropriate __init__.py."""
    cwd = pathlib.Path.cwd()
    mod_init = dirpath / "__init__.py"
    dirpath.mkdir(parents=True, exist_ok=True)
    if not mod_init.exists():
        mod_init.write_text(INIT)
    for directory in dirpath.parents:
        if directory == cwd:
            break
        (directory / "__init__.py").touch()


def cmd_add(sitepath, module, title):
    """Add a page.

    This creates the designated directories and files and updates the
    sitemap.
    """
    dirpath = module_to_path(module)
    create_dirs(dirpath)


def escape_braces(text, pattern=BRACE_RE):
    """Escape interpolated variables so they will not be expanded yet"""
    escaped = pattern.sub(r"{{\1}}", text)
    return escaped


def md_codeblock(match):
    """Substitution method to replace markdown code blocks with pygmented HTML."""
    lang, code = match.groups()
    try:
        lexer = pygments.lexers.get_lexer_by_name(lang)
    except ValueError:
        lexer = pygments.lexers.TextLexer()
    highlighted = pygments.highlight(code, lexer, FORMATTER)
    return highlighted
    # escaped = escape_braces(highlighted)
    # return escaped


def md_highlight(md):
    """Replace markdown code blocks with pygmented HTML."""
    highlighted = CODE_RE.sub(md_codeblock, md)
    return highlighted


def md_highlight_and_parse(content):
    """Code highlight then convert to HTML."""
    coded = md_highlight(content)
    html = md_parse(coded)
    return html


def md_parse(md):
    """A separate function that can be adapted to a particular Markdown implementation"""
    parsed = cmarkgfm.markdown_to_html(md, CMARK_FLAGS)
    return parsed


def module_to_path(module):
    """Convert module name to filesystem path."""
    modpath = pathlib.Path(module.replace(".", "/")).resolve()
    return modpath


@functools.lru_cache(maxsize=2)
def sitemap_read():
    """Load page information from sitemap file."""
    try:
        with SITEMAP.open() as handle:
            sitemap = json.load(handle)
    except FileNotFoundError:
        sitemap = {}
    return sitemap


def sitemap_update(sitepath, module, title):
    """Update sitemap file with page information."""
    sitemap = sitemap_read()
    sitemap[sitepath] = {
        "module": module,
        "title": title,
    }
    sitemap_write(sitemap)


def sitemap_write(sitemap):
    """Write page information to sitemap file."""
    with SITEMAP.open("w") as handle:
        json.dump(sitemap, handle)


def parse_args(args):
    """Parse command line args."""
    parser = argparse.ArgumentParser(description=__doc__, prog="enerator")
    subparsers = parser.add_subparsers(help="Available subcommands")
    parser_add = subparsers.add_parser("add", help=("create new page."),)
    parser_add.add_argument(
        "-m", "--module", type=str, help="module name, such as page.my_title",
    )
    parser_add.add_argument(
        "-t", "--title", type=str, help="title of the page",
    )
    parser_add.add_argument(
        "sitepath",
        type=pathlib.PurePosixPath,
        help="sitepath, such as /category/my_page/",
    )
    parser_add.set_defaults(func=cmd_add)

    if args:
        kwargs = vars(parser.parse_args(args))
        func = kwargs.pop("func")
        func(**kwargs)
    else:
        parser.print_help()


def main():
    """Run as script."""
    parse_args(sys.argv[1:])
