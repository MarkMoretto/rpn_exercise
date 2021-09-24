#!/usr/bin/python3
# -*- coding: utf-8 -*-


__all__ = [
    "RpnShell",
    ]

import re
import cmd


from ._rpn import Rpn
from ._types import StrList


# - Header and prompt formatting.
header_lines = [
    "\x1b[1;35mWelcome to the Reverse Polish Notation Calculator!\x1b[0m",
    "",
    "\x1b[6;33m***\x1b[0m \x1b[0;33mDe-luxe\x1b[0m \x1b[6;33m***\x1b[0m",
    "",
    "\x1b[0;33;40mType\x1b[0m \x1b[1;96mhelp\x1b[0m \x1b[0;33;40mfor list of available options.\x1b[0m",
    "",
    ]

PROMPT = "\x1b[0;36m~~> \x1b[0m"
HEADER = "\n" + "\n".join(header_lines)



def parse_arg(string: str) -> StrList:
    if not string is None and len(string) > 0:
        res = re.sub(r"[^0-9-\+/\*]+", "", string, flags = re.I)
        return list(res)


class RpnShell(cmd.Cmd):

    intro = HEADER
    prompt = PROMPT
    ruler = "-"
    rpn = Rpn()

    def default(self, line) -> None:
        """Runs if no specific command is provided by the user.
        """
        if line:
            _tmp = parse_arg(line)
            if len(_tmp) > 0:
                for el in _tmp:
                    self.rpn.execute_next(el)
        else:
            print("Please make sure to pass a numeric value or appropriate operator!\n")

    def emptyline(self, s):
        self.default(s)

    # - BEGIN: RPN
    def do_calc(self, arg):
        self.default(arg)

    def help_calc(self):
        lines = (
            "$ calc [arg(s)]",
            "Calculate an RPN expression",
            "", 
            "Example -",
            ">>> calc 23+",
            )
        print("\n".join(lines))

    def do_reset(self, arg) -> None:
        """Reset RPN state.
        """
        self.rpn.reset
        print("RPN state reset.")

    def do_state(self, arg) -> None:
        """Return current state of RPN instance.
        """
        print(self.rpn.status)

    def do_c(self, arg):
        """Alias for `reset`.
        """
        self.do_reset(arg)

    def do_del(self, arg):
        """Delete last item added to stack.
        """
        self.rpn.remove_last
        self.do_state(arg)

    def help_del(self):
        lines = "$ del", "Remove the last statement from the RPN stack."
        print("\n".join(lines))

    def do_operators(self, arg):
        self.rpn.descriptions()

    def do_add_expr(self, arg):
        """Placeholder for capability to add new expression
        into the instance.  Will only work for the current
        session being run.
        """
        pass

    # -/ END: RPN
    def do_exit(self, arg):
        print("Goodbye!")
        exit(0)