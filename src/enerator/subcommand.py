"""Helpers for command line parsing."""

import functools
import typing
from argparse import ArgumentParser
from argparse import _SubParsersAction as SubParsers  # noqa:WPS450


class Cmdargs(typing.NamedTuple):
    """Container for command line arguments."""

    args: typing.Tuple[str, ...]
    desc: str
    cast: typing.Optional[type] = str
    action: str = "store"
    default: typing.Any = None
    dest: typing.Optional[str] = None


@functools.lru_cache(maxsize=2)
def argparser() -> typing.Tuple[ArgumentParser, SubParsers]:
    """Set up argument parser.

    Returns:
        Tuple of ArgumentParser and subparsers
    """
    parser = ArgumentParser(
        description="Simple Static Site Generator using Python", prog="enerator"
    )
    subparsers = parser.add_subparsers(help="Available subcommands")
    return (parser, subparsers)


def parse_args(args: list) -> None:
    """Parse command line args.

    Args:
        args: list of arguments passed from commandline (sys.argv[1:])
    """
    parser, subparsers = argparser()

    if args:
        parsed_args = parser.parse_args(args)
        func = parsed_args.func
        func(parsed_args)
    else:
        parser.print_help()


def subcommand(arglist: typing.Tuple[Cmdargs, ...]) -> typing.Callable:
    """Decorate new subcommand.

    Args:
        arglist: list of arguments

    Returns:
        decorated function
    """
    _, subparsers = argparser()

    def decorator(func: typing.Callable) -> typing.Callable:
        description = (func.__doc__ or "No description").partition("\n")[0]
        parser = subparsers.add_parser(func.__name__, description=description)
        for arg in arglist:
            kwargs: typing.Dict[str, typing.Union[str, type]] = {
                "action": arg.action,
                "help": arg.desc,
            }
            if arg.default is not None:
                kwargs["default"] = arg.default
            if arg.dest is not None:
                kwargs["dest"] = arg.dest
            if arg.cast is not None:
                kwargs["type"] = arg.cast
            parser.add_argument(*arg.args, **kwargs)  # type: ignore
        parser.set_defaults(func=func)
        return func

    return decorator
