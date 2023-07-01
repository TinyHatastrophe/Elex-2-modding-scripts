import sys
import os
import shutil
import glob

import util.config as config
from util.util import STATUS_ERROR, STATUS_OK, DEBUG_ALL, DEBUG_FAST, start_timer, pause_timer
from util.console import print_error, print_debug, print_info
from util.elex2resman_wrapper import supported_ext

def is_dir(path):
    return os.path.isdir(path)

def is_file(path):
    return os.path.isfile(path)

def remove_file(file, thread=""):
    if not is_file(file):
        print_error(f"{thread}Tried to remove `{file}` as a file, script error?")
        return

    print_debug(DEBUG_ALL, f"{thread}Removing: `{file}`")
    os.remove(file)

def remove_dir(directory):
    if not is_dir(directory):
        print_error(f"Tried to remove `{directory}` as a file, script error?")
        return

    print_debug(DEBUG_FAST, f"Removing: `{directory}`")
    shutil.rmtree(directory)

def move_dir(old_dir, new_parent_dir, thread=""):
    print_debug(DEBUG_FAST, f"{thread}Moving `{old_dir}` to `{new_parent_dir}`")
    shutil.move(old_dir, new_parent_dir)

def get_dir_from_arg(index, required=True):
    try:
        directory = sys.argv[index]
    except IndexError:
        if required:
            print_error(f"Missing argument number {index}, expected dir")
        return None

    if not is_dir(directory):
        print_error(f"Parsed argument '{directory}' not a directory, for files you can use elexresman directly")
        return None

    return directory

def get_parent_dir(path):
    return os.path.dirname(path)

def create_dir(path, name):
    if not is_dir(path):
        print_error(f"Tried to create folder `{name}`, but `{path}` isn't correct location")
        return None

    new_dir = os.path.join(path, name)

    if is_dir(new_dir):
        if config.current.get("overwrite"):
            print_info(f"Found old folder `{new_dir}`, cleaning it")

            pause_timer()
            remove_dir(new_dir)
            start_timer()
        else:
            print_error("Tried to create `{new_dir}` but it already exist, either change config to allow for file "
                        "overwriting, or manually move/remove/rename this folder and run script again")
            return None

    os.mkdir(new_dir)
    print_debug(DEBUG_FAST, f"Created directory: `{new_dir}`")

    return new_dir

def get_file_size(file):
    file_stats = os.stat(file)

    size = file_stats.st_size / (1024 * 1024)

    return size

def get_location(path):
    return os.path.dirname(os.path.realpath(path))

def get_all_files_with_ext(directory, supported_ext):
    file_list = []

    for root, _, files in os.walk(directory):
        for name in files:
            file_ext = name.split(".")[-1]
            if file_ext in supported_ext:
                path = os.path.join(root, name)
                file_list.append(path)

    return file_list

def get_all_pak(directory):
    return get_all_files_with_ext(directory, ["pak"])

def get_all_elex2resman_supported_files(directory):
    return get_all_files_with_ext(directory, supported_ext)