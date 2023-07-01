import json

import util.console as console
import util.dirman as dirman
from util.util import STATUS_ERROR, STATUS_OK

# default config, if config.json is not found
current = {
    # global path to where elex2resman is (inlcuding *.exe name, with `/` instead of '\')
    "elex2resman_path": "C:/modding/Elex_2/tools/elex2resman_slightly_broken.exe",
    # impacts how much is printed on console
    # level 0: only most important stuff is printed
    # level 1: common debug information
    # level 2: print all debug information (can increase execution time)
    "debug_level": 1,
    # boolean, decides if scripts should try to overwrite files previously created by them
    # if false, manual cleaning will be needed between script executions
    # files created by elex2resman are always overwritten (because that's how elex2resman works)
    "overwrite": True,
    # defines maximum number of threads that can be used by the script for simultaneous job (like unpacking and
    # converting files)
    # set to 0 to disable multithreading
    "max_threads": 16
}

def verify_elex2resman():
    dirman.is_file(current["elex2resman_path"])

def read_config():
    """Reads config from file"""
    global current

    try:
        with open("config.json", "r") as file:
            current = json.load(file)
    except FileNotFoundError:
        console.print_warning("`config.json` not found, using defaults")

    if not verify_elex2resman():
        return STATUS_ERROR

    return STATUS_OK
