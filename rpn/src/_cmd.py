#!/usr/bin/python3
# -*- coding: utf-8 -*-


__all__ = [
    "RpnShell",
    ]

import re
import cmd
from os import linesep

from ._rpn import Expression, Rpn
from ._types import StrList
from ._colors import SGRColors as C

# - Header and prompt formatting.
header_lines = [
    f"{C.purple_lt}Welcome to the Reverse Polish Notation Calculator!{C.end}",
    "",
    f"{C.yel_blink}***{C.end} {C.yellow}De-luxe{C.end} {C.yel_blink}***{C.end}",
    "",
    f"{C.yellow}Type{C.end} {C.cyan_lt}help{C.end} {C.yellow}for list of available options.{C.end}",
    f"{C.yellow}Press{C.end} {C.blue_lt}q{C.end} {C.yellow}or{C.end} {C.blue_lt}exit{C.end} {C.yellow}to exit program.{C.end}",
    "",
    ]    

PROMPT = f"{C.cyan}~~> {C.end}"
HEADER = "\n" + "\n".join(header_lines)

RPN = Rpn()
OPERATORS_ALL = RPN.NUMBERS.union(RPN.operators)


def exit_program():
    println(f"{linesep}Goodbye!")
    exit(0)

def parse_arg(string: str, opers: set = OPERATORS_ALL) -> StrList:
    """Returns list of characters from a string that are valid
    operators or numeric values.

    Parameters
    ----------
    string : str
        Input string object to parse.
    opers : set
        Set of operators to validate each character against.
    
    Returns
    -------
    StrList
        List of string objects.
    """
    if not string is None and len(string) > 0:
        res = "".join([c for c in string if c in opers])
        return list(res)

def println(obj: str, *args, **kwargs) -> None:
    """"""
    print(f"{obj}{linesep}", *args, **kwargs)

class RpnShell(cmd.Cmd):

    intro = HEADER
    prompt = PROMPT
    ruler = "-"
    rpn = RPN

    def default(self, line) -> None:
        """Runs if no specific command is provided by the user.
        """
        if line:
            if line == "EOF":
                exit_program()

            _tmp = parse_arg(line)
            if len(_tmp) > 0:
                for el in _tmp:
                    self.rpn.execute_next(el)
        else:
            println("Please make sure to pass a numeric value or appropriate operator!\n")

    def emptyline(self):
        exit_program()
        # if s:
        #     self.default(s)
        # else:
        #     exit_program()

    # - BEGIN: RPN
    def do_calc(self, arg):
        if len(self.rpn.stacker) == 1:
            println(f"Result: {self.rpn.stacker[-1]}")
        else:
            self.default(arg)

    def help_calc(self):
        lines = (
            "$ calc [arg(s)]",
            "Calculate an RPN expression",
            "", 
            "Example -",
            ">>> calc 23+",
            )
        print(f"{linesep}".join(lines))

    def do_reset(self, arg) -> None:
        """Reset RPN state.
        """
        self.rpn.reset
        println("RPN state reset.")

    def do_state(self, arg) -> None:
        """Return current state of RPN instance.
        """
        println(self.rpn.status)

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
        print(f"{linesep}".join(lines))

    def do_operators(self, arg):
        self.rpn.descriptions()

    def help_operators(self):
        lines = """Display list of currently available operators
        within the program.
        """.strip().split(linesep)
        print(f"{linesep}".join(lines))       

    # -/ END: RPN
    def do_q(self, arg):
        """Alias for `exit`
        """
        self.do_exit(arg)
        
    def do_exit(self, arg):
        """Exit program with return code 0.
        """
        exit_program()



    #TODO: Implement ability to add expression.
    # def do_add_expr(self, arg):
    #     """Work in progress."""
        # gcd lambda a, b: mathgcd(b, a)
        # _tmp = arg.split(" ", maxsplit = 1)
        # if len(_tmp) == 2:
        #     _sig, _func = [str(s).strip() for s in _tmp]
        #     print(_sig, _func)
        #     self.rpn.add_expression(_sig, _func)
        #     print(f"Added operator {_sig} into cache.")


    # def help_add_expr(self, arg):
    #     lines = """Create and add function into the mix.

    #     Arguments
    #     ---------
    #     arg : str
    #         Line in command prompt. First argumetn should be sign or 
    #         operator name/alias.
    #         Second argument should be lambda function with appropriate arguments.
    #             Current standard library packages available are:
    #                 math
    #                 statistics
    #     """.strip().split("\n")
    #     print("\n".join(lines))         