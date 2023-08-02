import argparse
import sys

import lark

from urn import __version__


def parse_args() -> argparse.Namespace:
    """Parse CLI args."""
    argparser = argparse.ArgumentParser(prog="urn", description="Calculator.")
    argparser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    command_source = argparser.add_mutually_exclusive_group()
    command_source.add_argument("-c", "--command", help="Command string to evaluate")
    command_source.add_argument("-f", "--filename", help="Read command string from file and evaluate")
    return argparser.parse_args()


def main() -> None:
    """Entrypoint."""
    args = parse_args()

    # Delay expensive imports until needed.
    from urn.shell import run_shell
    from urn.evaluation import process_query

    command_parser = lark.Lark.open("grammar.lark", rel_to=__file__)

    if args.command or args.filename:
        
        if args.filename:
            with open(args.filename) as f:
                command = f.read()
        else:
            command = args.command
        try:
            print(process_query(command_parser, command))
        except lark.exceptions.LarkError as error:
            print(f"Command parsing error: {error}", file=sys.stderr)
            sys.exit(1)
    else:
        run_shell(command_parser)


if __name__ == "__main__":
    main()
