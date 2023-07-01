import threading
from textwrap import wrap

import util.config as config
from util.util import start_timer, pause_timer, DEBUG_ALL, DEBUG_FAST

"""Contains all stuff related to printing on console"""

# ansi codes
COLOR_NONE = 0
COLOR_RED = 31
COLOR_GREEN = 32
COLOR_YELLOW = 33
COLOR_BLUE = 34

# used to synchronize multiple threads printing to console
lock = None

def print_colored(msg, color, thread=""):
    """Print message in specific color, wrapped to fit 120 collums"""
    global lock

    msg = wrap(msg, 120)

    if lock:
        lock.acquire()

    for line in msg:
        print(f"\x1b[1;{color}m" + line + "\x1b[0m")

    if lock:
        lock.release()

def print_debug(debug_level, msg):
    """Print message in `debug` color if config is set to print debug messages"""
    if debug_level <= config.current.get("debug_level"):
        print_colored(msg, COLOR_BLUE)

def print_warning(msg):
    """Print message in warning-y yellow, used to warn user about stuff"""
    print_colored(msg, COLOR_YELLOW)

def print_error(msg):
    """Print message in error-y red, used to report errors"""
    print_colored(msg, COLOR_RED)

def print_success(msg):
    """Print message in successful green, used to inform about success"""
    print_colored(msg, COLOR_GREEN)

def print_info(msg):
    """Print message without coloring it, used to inform about what is currently going on"""
    print_colored(msg, COLOR_NONE)

def wait_for_confirmation():
    """Used to make sure user what was printed, before continuing."""
    pause_timer()
    input("\nPress enter to continue...")
    print("")
    start_timer()

def create_lock():
    global lock

    lock = threading.Lock()
