"""Tests for enerator."""


import sys
from argparse import Namespace

from enerator.subcommand import Cmdargs, parse_args, subcommand

FILENAME = "/file.json"


@subcommand(
    (
        Cmdargs(
            ("-f", "--filename"),
            "The Filename, please",
            default=FILENAME,
            dest="filepath",
        ),
    )
)
def show(args: Namespace) -> None:
    sys.stdout.write(f"{args.filepath}\n")


def test_cmdargs(capsys) -> None:
    cmd_args = ["show"]
    parse_args(cmd_args)
    captured = capsys.readouterr()
    assert FILENAME in captured.out
