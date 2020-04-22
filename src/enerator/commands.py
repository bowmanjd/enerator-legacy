"""Commandline parsers and functions."""


import argparse
import pathlib
import sys

from enerator.generate import generate
from enerator.sitemap import sitemap_update

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


def create_dirs(dirpath: pathlib.Path) -> None:
    """Create directories and populate with appropriate __init__.py.

    Args:
        dirpath: a pathlib Path.

    """
    cwd = pathlib.Path.cwd()
    mod_init = dirpath / "__init__.py"
    dirpath.mkdir(parents=True, exist_ok=True)
    if not mod_init.exists():
        mod_init.write_text(INIT)
    for directory in dirpath.parents:
        if directory == cwd:
            break
        (directory / "__init__.py").touch()


def cmd_add(args: argparse.Namespace) -> None:
    """Add a page.

    This creates the designated directories and files and updates the
    sitemap.

    Args:
        args: a Namespace object returned from argparse parser.
    """
    dirpath = module_to_path(args.module)
    create_dirs(dirpath)
    sitemap_update(args.sitepath, args.module, args.title)


def cmd_gen(args: argparse.Namespace) -> None:
    """Generate page(s).

    Args:
        args: a Namespace object returned from argparse parser.
    """
    generate(args.module)


def module_to_path(module: str) -> pathlib.Path:
    """Convert module name to filesystem path.

    Args:
        module: string form of Python module name

    Returns:
        a pathlib Path for the directory structure corresponding
        to the module name
    """
    return pathlib.Path(module.replace(".", "/")).resolve()


def parse_args(args: list) -> None:
    """Parse command line args.

    Args:
        args: list of arguments passed from commandline (sys.argv[1:])
    """
    parser = argparse.ArgumentParser(description=__doc__, prog="enerator")
    subparsers = parser.add_subparsers(help="Available subcommands")
    parser_add = subparsers.add_parser("add", help=("create new page."))
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

    parser_gen = subparsers.add_parser(
        "generate", aliases=["gen"], help=("generate all pages or a single page")
    )
    parser_gen.add_argument(
        "-m", "--module", type=str, help="a single, existing module to generate",
    )
    parser_gen.set_defaults(func=cmd_gen)

    if args:
        parsed_args = parser.parse_args(args)
        func = parsed_args.func
        func(parsed_args)
    else:
        parser.print_help()


def main() -> None:
    """Run as script."""
    parse_args(sys.argv[1:])
