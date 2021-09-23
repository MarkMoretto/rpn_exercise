#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ANSI esC_ape C_ode C_olors
See: https://en.wikipedia.org/wiki/ANSI_escape_code

Main color codes and ranges:
    0 - black
    1 - red
    2 - green
    3 - yellow
    4 - blue
    5 - purple
    6 - beige
    7 - white
    30-39 - foreground color
    40-49 - backgrond color
"""

class BColors:
    C_END      = "\33[0m" # End statement
    C_BOLD     = "\33[1m"
    C_ITALIC   = "\33[3m"
    C_URL      = "\33[4m"
    C_BLINK    = "\33[5m"
    C_BLINK2   = "\33[6m"
    C_SELECTED = "\33[7m"

    C_BLACK  = "\33[30m"
    C_RED    = "\33[31m"
    C_GREEN  = "\33[32m"
    C_YELLOW = "\33[33m"
    C_BLUE   = "\33[34m"
    C_VIOLET = "\33[35m"
    C_BEIGE  = "\33[36m"
    C_WHITE  = "\33[37m"

    C_BLACKBG  = "\33[40m"
    C_REDBG    = "\33[41m"
    C_GREENBG  = "\33[42m"
    C_YELLOWBG = "\33[43m"
    C_BLUEBG   = "\33[44m"
    C_VIOLETBG = "\33[45m"
    C_BEIGEBG  = "\33[46m"
    C_WHITEBG  = "\33[47m"

    C_GREY    = "\33[90m"
    C_RED2    = "\33[91m"
    C_GREEN2  = "\33[92m"
    C_YELLOW2 = "\33[93m"
    C_BLUE2   = "\33[94m"
    C_VIOLET2 = "\33[95m"
    C_BEIGE2  = "\33[96m"
    C_WHITE2  = "\33[97m"

    C_GREYBG    = "\33[100m"
    C_REDBG2    = "\33[101m"
    C_GREENBG2  = "\33[102m"
    C_YELLOWBG2 = "\33[103m"
    C_BLUEBG2   = "\33[104m"
    C_VIOLETBG2 = "\33[105m"
    C_BEIGEBG2  = "\33[106m"
    C_WHITEBG2  = "\33[107m"




# def print_reds():
#     for c in range(8):
#         line = [f"\x1b[{i};3{i};4{i}m\x1b[0m" for i in range(8)]
#         print(line)
# print_reds()

# txt = "Hello"
# print(C_RED + txt + C_END)
def print_format_table():
    """prints table of formatted text format options
    0 - black
    1 - red
    2 - green
    3 - yellow
    4 - blue
    5 - purple
    6 - beige
    7 - white
    30 + above == foreground color
    40 + above = backgrond color

    print("\x1b[6;30;42mH\x1b[0m" + "elp")
    """
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print("\n")
# print_format_table()


def print_c_format_table():
    for i in range(11):
        for j in range(10):
            n = 10*i + j
            if n <= 108:
                print(f"\033[{n}m {n:>3}\033[m", sep=" ", end = " ")
        print()
# print_c_format_table()

