'''
Miscellaneous functions for debugging
'''

import sys


RED_BOLD = '\x1b[1;31m'
GREEN_BOLD = '\x1b[1;32m'
BLUE_BOLD = '\x1b[1;34m'
RESET = '\x1b[0m'


def print_red(msg: str):
    '''Prints the `msg` in bold red'''
    sys.stdout.write(RED_BOLD + msg + RESET + '\n')


def print_green(msg: str):
    '''Prints the `msg` in bold green'''
    sys.stdout.write(GREEN_BOLD + msg + RESET + '\n')


def print_blue(msg: str):
    '''Prints the `msg` in bold blue'''
    sys.stdout.write(BLUE_BOLD + msg + RESET + '\n')
