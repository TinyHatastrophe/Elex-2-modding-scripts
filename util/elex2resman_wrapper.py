from subprocess import run

import util.config as config
import util.dirman as dirman
from util.console import print_debug, print_info
from util.util import STATUS_ERROR, STATUS_OK, DEBUG_FAST, DEBUG_ALL

supported_ext = [
    "pak",
    "hdr",
    "elex2img",
    "elex2snd",
#    "elex2dlg", # not supported anymore? seems to be causing problems
    "elex2tpl",
    "elex2wrl",
    "elex2sec",
    "elex2secmod"
]

def elex2resman_do_your_magic(file, thread=""):
    # ignore file types elex2resman can't convert
    file_ext = file.split(".")[-1]
    if file_ext not in supported_ext:
        print_debug(DEBUG_FAST, f"{thread}Ignored file `{file}` while converting, not supported by elex2resman")
        return STATUS_ERROR

    size = round(dirman.get_file_size(file))
    if size >= 1024:
        print_info(f"{thread}Unpacking very big file ({size} MB), this will take a while")

    cmd = config.current["elex2resman_path"] + f" \"{file}\" --non-interactive"
    print_debug(DEBUG_ALL, f"{thread}Calling: `{cmd}`")
    result = run(cmd, capture_output=True)
    if result.stdout == b'The archive is empty.\r\n':
        print_debug(DEBUG_FAST, f"{thread}Ignored file: `{file}, archive is empty")
        return STATUS_ERROR

    return STATUS_OK