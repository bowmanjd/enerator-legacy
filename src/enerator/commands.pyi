import argparse
import pathlib

INIT: str

def create_dirs(dirpath: pathlib.Path) -> None: ...
def cmd_add(args: argparse.Namespace) -> None: ...
def module_to_path(module: str) -> pathlib.Path: ...
def parse_args(args: list) -> None: ...
def main() -> None: ...