"""Helpers useful for any tests."""

import os
import sys


def set_path(path: os.PathLike) -> None:
    """Change to specified directory and adjust path.

    Args:
        path: path to working directory
    """
    os.chdir(path)
    sys.path = ["", *sys.path]
