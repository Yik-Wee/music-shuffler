'''
Miscellaneous functions for debugging
'''

import sys


RED_BOLD = '\x1b[1;31m'
GREEN_BOLD = '\x1b[1;32m'
RESET = '\x1b[0m'


def print_red(msg: str):
    '''Prints the `msg` in bold red for debugging'''
    sys.stdout.write(RED_BOLD + msg + RESET + '\n')


def print_green(msg: str):
    '''Prints the `msg` in bold green for debugging'''
    sys.stdout.write(GREEN_BOLD + msg + RESET + '\n')
