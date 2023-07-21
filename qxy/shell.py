import cmd

import lark

from qxy.evaluation import process_query


EOL = ";"
PROMPT = "QXY> "
PROMPT_CONTINUATION = "...  "


class QxyShell(cmd.Cmd):
    """QXY shell."""
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

    def default(self, line: str) -> str:
        try:
            print(self._process_input(line))
        except Exception as error:
            print(f"Error: {error}")

    def do_quit(self, _) -> bool:
        print("Exiting QXY shell.")
        return True
    
    def emptyline(self) -> None:
        # Override method: empty line should not execute previous command.
        pass

    def _process_input(self, query: str) -> str:
        return process_query(self.parser, query)


def run_shell(parser: lark.Lark) -> None:
    """Run QXY shell."""
    QxyShell(parser=parser).cmdloop()
