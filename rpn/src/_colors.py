#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: ANSI esCape Code Color script.

See: https://en.wikipedia.org/wiki/ANSI_escape_code
See: https://en.wikipedia.org/wiki/C0_and_C1_control_codes
See: https://en.wikipedia.org/wiki/Escape_character#ASCII_escape_character


~*~ SGR (Select Graphic Rendition) parameters ~*~

Base color codes:
    0 - black
    1 - red
    2 - green
    3 - yellow
    4 - blue
    5 - purple
    6 - beige
    7 - white

General pattern:
    ESC[(a);(b);(c)m(d)ESC[0m

Where -
    ESC = ASCII escape character**
        \033    - Octal
        \x1b    - Hexadecimal
        ^[      - Hexadecimal
        27      - Decimal

    
    (a) = 0 - 7
        Refers to special text attributes (e.g. - bold, italic).

    (b) = 30 - 37
        Set foreground color.

    (c) = 40 - 47
        Set background color.

    (d) = Text to influence.

** See: https://en.wikipedia.org/wiki/C0_and_C1_control_codes
"""

class SGRColors:
    # End statement for color section
    # Can be used in concert with the remaining options,
    # but should not be used to start a sequence.    
    end = "\033[0m"

    purple = "\033[35m"
    purple_lt = "\033[95m"
    purp_lt_blink = "\033[6;95m"

    yellow = "\033[33m"
    yellow_lt = "\033[93m"    
    yel_blink = "\033[6;33m"

    cyan = "\033[36m"
    cyan_blink = "\033[6;36m"

    cyan_lt = "\033[96m"
    cyan_lt_blink = "\033[6;96m"

    red = "\033[31m"
    red_lt = "\033[1;31m"
    red_blink = "\033[6;31m"

    green = "\033[32m"
    green_lt = "\033[92m"    
    grn_blink = "\033[6;32m"

    blue = "\033[34m"
    blue_lt = "\033[94m"


############################
# - Color demo functions - #
############################

def print_format_table() -> None:
    """Prints table of formatted text format options
    print("\x1b[6;30;42mH\x1b[0m" + "elp")
    """
    for style in range(8):
        for fg in range(30, 38):
            s = ""
            for bg in range(40, 48):
                output = ';'.join([str(style), str(fg), str(bg)])
                s += f"\x1b[{output}m%{output}\x1b[0m"
            print(s)
        print("\n")


def print_c_format_table():
    """Same as print_format_table, but limited in scope.
    """
    for i in range(11):
        for j in range(10):
            n = 10*i + j
            if n <= 108:
                print(f"\033[{n}m {n:>3}\033[m", sep=" ", end = " ")
        print()


