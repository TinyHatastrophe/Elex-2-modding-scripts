from time import time
from math import floor, ceil

import util.console as console

STATUS_OK = 0
STATUS_ERROR = -1

DEBUG_FAST = 1
DEBUG_ALL = 2

start_time = None
pause_time = None

def start_timer():
    global start_time
    global pause_time

    if start_time and pause_time:
        pause_length = time() - pause_time
        start_time += pause_length

    start_time = time()

def calculate_elapsed_time():
    global start_time

    if not start_time:
        console.print_error("Can't calculate elapsed time, because timer was never started")
        return

    elapsed_time = time() - start_time

    minutes = floor(elapsed_time/60)
    seconds = ceil(elapsed_time%60)

    return minutes, seconds

def pause_timer():
    global start_time
    global pause_time

    if not start_time:
        console.print_error("Timer cannot be stopped! Not because it's invetiable, but because it was never started")
        return

    pause_time = time()
