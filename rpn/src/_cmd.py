#!/usr/bin/python3
# -*- coding: utf-8 -*-


__all__ = [
    "RpnShell",
    ]

import re
import cmd
import subprocess
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

# Instance Rpn() class
RPN = Rpn()


def exit_program():
    println(f"{linesep}Goodbye!")
    exit(0)

def parse_arg(string: str) -> StrList:
    """Returns list of characters from a string that are valid
    operators or numeric values.

    Parameters
    ----------
    string : str
        Input string object to parse.

    Returns
    -------
    StrList
        List of string objects.
    """
    if string and len(string) > 0:
        string = RPN.clean_up_whitespace(string)

        # if len(string) == 2 and RPN.is_number(string):
        #     return [string]

        res = " ".join([c for c in string.split() if c in RPN.operators or RPN.is_number(c)])
        return list(res.split())


def toggle_first_entry(rpn_cls: Rpn, min_numbers = 2) -> bool:
    """If stack meets and/or exceeds min_numbers threshold, then 
    return True, else False.
    After two numbers are reached, barring special circumstances,
    any subsequent entries should include an operator and produce
    a "final" number.  Or, at least an interim final number.
    """
    _result = True
    if len(rpn_cls.status) > 0:
        _result = sum([1 if rpn_cls.is_number(item) else 0 for item in rpn_cls.status]) >= min_numbers
    return _result

def println(obj: str) -> None:
    """Print to standard output with a newline character attached
    to the end of the object.
    """
    print(f"{obj}{linesep}")

def printh(iterable) -> None:
    """Print multiline `help` documentation to stdout.
    """
    print(f"{linesep}".join(iterable))


# Keep history alive unless 'do_ce()' called
PERSIST = []

class RpnShell(cmd.Cmd):
    """RpnShell class.  This is the main 'driver' class for the 
    rpn program.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    intro = HEADER
    prompt = PROMPT
    ruler = "-"
    rpn = RPN
    first_entry = False
    persist = PERSIST.copy()

    def default(self, line) -> None:
        """Runs if no specific command is provided by the user.
        """
        
        if line:
            if line == "EOF":
                exit_program()

            print(f"{C.yellow_lt}{line}{C.end}")

            # Clean-up arguments
            _tmp = parse_arg(line)

            # If more than one argument found, pass each
            # individually for evaluation and updating of
            # current state.
            if len(_tmp) > 0:
                # add to persistent history
                self.persist.extend(_tmp)    

                for el in _tmp:
                    g, msg = self.rpn.execute_next(el)
                    if g != 0:
                        print(msg)
                        break

                # Toggle first_entry variable.
                # Populated stack is required            
                self.first_entry = toggle_first_entry(self.rpn)
                print(self.first_entry, self.rpn.status)
                # else:
                #     self.do_calc(None)


    def emptyline(self) -> None:
        """If enter/return pressed with no value or command,
        exit the program.
        """
        exit_program()

    # - BEGIN: Actions
    def do_calc(self, arg) -> None:
        if self.first_entry:
            self.default(arg)
        else:
            self.do_result(None)

    
    def do_del(self, arg) -> None:
        """Delete last item added to stack.
        """
        self.rpn.remove_last
        self.do_state(arg)

    def do_history(self, arg) -> None:
        """Print persistent history to stdout.
        """
        _out = "No history to report!"
        if len(self.persist) > 0:
            _out = ", ".join(self.persist)
        print(_out)

    def do_operators(self, arg) -> None:
        self.rpn.descriptions()

    def do_result(self, arg) -> None:
        """Determine output and send to stdout.
        """
        print(f"{C.grn_blink}Result: {self.rpn.result}{C.end}")


    def do_reset(self, arg) -> None:
        """Reset RPN state.
        """
        self.rpn.reset
        print("RPN state reset.")

    def do_state(self, arg) -> None:
        """Return current state of RPN instance.
        """
        print(self.rpn.status)

    # -/ END: Actions


    # - BEGIN: Aliases
    def do_ans(self, arg) -> None:
        """Alias for `calc`.
        """
        self.do_calc(None)

    def do_c(self, arg):
        """Alias for `reset`.
        """
        self.do_reset(None)

    def do_ce(self, arg):
        """Alias for `reset` Does "deeper" clear
        of all persistent history.
        """
        self.persist.clear()
        self.do_reset(None)    

    def do_ops(self, arg):
        """Alias for `operators`.
        """
        self.do_operators(None)

    # -/ END: Aliases


    # - BEGIN: Runtime
    def do_clear(self, intro=None):
        try:
            subprocess.check_call("clear", stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            print(e)

    def do_q(self, arg):
        """Alias for `exit`
        """
        self.do_exit(arg)
        
    def do_exit(self, arg):
        """Exit program with return code 0.
        """
        exit_program()

    def do_restart(self, intro=None):
        self.persist.clear()
        self.do_reset(None)
        self.do_clear()
        RpnShell().cmdloop()
        # return cmd.Cmd.cmdloop(self, intro)
    
    def do_EOF(self, line):
        return True
    # -/ END: Runtime


    # - BEGIN: Help
    def help_calc(self):
        lines = (
            "$ calc [arg(s)]",
            "Calculate an RPN expression",
            "", 
            "Example -",
            ">>> calc 23+",
            )
        print(lines)

    def help_del(self):
        lines = "$ del", "Remove the last statement from the RPN stack."
        printh(lines)

    def help_operators(self):
        lines = """Display list of currently available operators
        within the program.
        """.strip().split(linesep)
        print(f"{linesep}".join(lines))       

    def help_clear(self):
        lines = "$ clear", "Clear current prompt."
        printh(lines)

    def help_restart(self):
        lines = "$ restart", "Restart program.", "NOTE: This clears history and current stack."
        printh(lines)        
    # -/ END: Help
