import cmd
import sys

import lark

from urn.computation import ComputationDescriptionError
from urn.evaluation import process_query


EOL = ";"
PROMPT = "urn> "
PROMPT_CONTINUATION = " " * len(PROMPT)


class UrnShell(cmd.Cmd):
    """urn shell."""
    prompt = PROMPT

    def __init__(self, parser: lark.Lark) -> None:
        super().__init__()
        self.parser = parser
        self.multiline_input = []

    def precmd(self, line: str) -> str:

        self.multiline_input.append(line)

        if line.endswith(EOL):
            self.prompt = PROMPT
            line = "\n".join(self.multiline_input)
            self.multiline_input = []
            
        else:
            self.prompt = PROMPT_CONTINUATION
            line = ""

        return line

    def default(self, line: str) -> None:
        try:
            print(self._process_input(line))
        except ComputationDescriptionError as error:
            print(f"Computation error: {error}", file=sys.stderr)
        except lark.exceptions.LarkError as error:
            print(f"Parser error: {error}", file=sys.stderr)

    def do_quit(self, _) -> bool:
        print("Exiting urn shell.")
        return True
    
    def emptyline(self) -> None:
        # Override method: empty line should not execute previous command.
        pass

    def _process_input(self, query: str) -> str:
        return process_query(self.parser, query)
