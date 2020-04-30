"""Commandline parsers and functions."""

import pathlib
import sys
from argparse import Namespace

import enerator.add
import enerator.generate
from enerator.subcommand import Cmdargs, parse_args, subcommand


@subcommand(
    (
        Cmdargs(("-m", "--module"), "module name, such as page.my_title"),
        Cmdargs(("-t", "--title"), "title of the page"),
        Cmdargs(
            ("sitepath",),
            "sitepath, such as /category/my_page/",
            pathlib.PurePosixPath,
        ),
    )
)
def add(args: Namespace) -> None:
    """Add a page.

    This creates the designated directories and files and updates the
    sitemap.

    Args:
        args: a Namespace object returned from argparse parser.
    """
    dirpath = enerator.add.add(args.sitepath, args.module, args.title)
    sys.stdout.write(f"{dirpath}\n")


@subcommand(
    (
        Cmdargs(("-m", "--module"), "module name, such as page.my_title"),
        Cmdargs(("-o", "--output"), "directory for static site output", pathlib.Path),
    )
)
def gen(args: Namespace) -> None:
    """Generate page(s).

    Args:
        args: a Namespace object returned from argparse parser.
    """
    output_path = enerator.generate.generate(args.module, args.output)
    sys.stdout.write(f"{output_path}\n")


def main() -> None:
    """Run as script."""
    parse_args(sys.argv[1:])
