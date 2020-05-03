"""Commandline parsers and functions."""

import pathlib
import sys
from argparse import Namespace

import enerator.add
import enerator.generate
from enerator.subcommand import Cmdargs, parse_args, subcommand


@subcommand(
    (
        Cmdargs(("module",), "module name, such as page.my_title"),
        Cmdargs(("-t", "--title"), "title of the page"),
        Cmdargs(
            ("-s", "--sitepath",),
            "sitepath, such as /category/my_page/",
            pathlib.PurePosixPath,
        ),
        Cmdargs(
            ("-n", "--nositemap"),
            "only generate files, do not update sitemap (for templates)",
            cast=None,
            action="store_false",
            dest="sitemap",
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
    print(args.sitemap)
    dirpath = enerator.add.add(args.module, args.sitepath, args.sitemap)
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
