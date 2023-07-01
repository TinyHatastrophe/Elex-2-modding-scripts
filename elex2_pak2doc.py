import os
import concurrent.futures
import math

import util.config as config
import util.console as console
import util.dirman as dirman
from util.util import STATUS_ERROR, STATUS_OK, start_timer, calculate_elapsed_time, DEBUG_FAST, DEBUG_ALL
from util.elex2resman_wrapper import elex2resman_do_your_magic

"""Takes Elex 2 directory as first argument, and output directory as optional second argument. Unpacks all .pak Elex 2
   files, and convert them all to human readable files using elex2resman. Files that elex2resman can't convert are being
   ignored."""

# relative path to .pak files
rel_pak_path = {
    "dx11": ("ELEX2DX11", "data", "packed"),
    "dx12": ("data", "packed")
}

unpack_path = {
    "dx11": "dx11",
    "dx12": "dx12"
}

DX11_PATH = ("ELEX2DX11", "data", "packed")
DX12_PATH = ("data", "packed")

def pak_unpack(file, thread=""):
    console.print_info(f"{thread}Unpacking: `{file}`")

    filename = os.path.basename(file)
    if not filename.endswith(".pak"):
        console.print_warning(f"{thread}`{filename}` is not correct .pak file, ignoring")
        return None

    if not filename.startswith("c_"):
        console.print_warning(f"{thread}`{filename}` is probably a mod file, ignoring")
        return None

    # ignore if elex2resman can't unpack
    ret = elex2resman_do_your_magic(file, thread)
    if ret != STATUS_OK:
        return None

    unpacked_dir = file.removesuffix(".pak")
    location = dirman.get_location(file)
    unpacked_path = os.path.join(location, unpacked_dir)

    if not dirman.is_dir(unpacked_path):
        console.print_error(f"{thread}Unpacking of `{file}` failed")
        return None

    return unpacked_path

def pak_handler(file, target_dir, thread=""):
    if thread:
        console.print_info(f"{thread}thread started")

    unpacked_pak = pak_unpack(file, thread)
    if unpacked_pak:
        dirman.move_dir(unpacked_pak, target_dir, thread)

    if thread:
        console.print_info(f"{thread}thread finished")

def prepare_unpacked_folder(target_dir):
    unpacked_dir = dirman.create_dir(target_dir, "unpacked")
    if not unpacked_dir:
        return None

    ret = dirman.create_dir(unpacked_dir, "dx11")
    if not ret:
        return None

    ret = dirman.create_dir(unpacked_dir, "dx12")
    if not ret:
        return None

    return unpacked_dir

def get_pak_location(elex2_dir):
    abs_pak_path = {}
    for dx, path in rel_pak_path.items():
        abs_path = os.path.join(elex2_dir, *path)

        if not dirman.is_dir(abs_path):
            console.print_error(f"'{abs_path} is not correct directory")
            return None

        abs_pak_path[dx] = abs_path

    return abs_pak_path

def unpack_all_pak(abs_pak_path, unpacked_dir):
    console.print_info("Step 1. Unpacking *.pak files")
    for dx, path in abs_pak_path.items():
        console.print_info(f"Working on {dx} *.pak location: `{path}`")

        target_dir_dx = os.path.join(unpacked_dir, dx)

        pak_list = dirman.get_all_pak(path)

        workers = config.current.get("max_threads")
        if not workers:
            for file in pak_list:
                pak_handler(file, target_dir_dx)
        else:
            futures = []

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                for i, file in enumerate(pak_list):
                    future = executor.submit(pak_handler, file, target_dir_dx, f"[THREAD {i}]:")
                    futures.append(future)

            concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

    console.print_info("Unpacking *.pak files finished")

def group_elements(my_list, group_size):
    job_list = []
    elements_per_job = math.ceil(len(my_list)/group_size)

    for i in range(group_size):
        first_index = i*elements_per_job
        last_index = min(len(my_list), (i+1)*elements_per_job)

        job = my_list[first_index:last_index+1]
        job_list.append(job)

    return job_list

def convert_handler(file_list, thread=""):
    if thread:
        console.print_info(f"{thread}thread started")

    for file in file_list:
        console.print_debug(DEBUG_ALL, f"{thread}Working on a file: `{file}`")

        # remove original file only if conversion was a success
        # ignore if there was no conversion - because not all files are supported by elex2resman
        ret = elex2resman_do_your_magic(file, thread)
        if ret == STATUS_OK:
            dirman.remove_file(file)

    if thread:
        console.print_info(f"{thread}thread started")

def convert_all_to_doc(directory):
    console.print_info("Step 2. Converting all supported files")
    file_list = dirman.get_all_elex2resman_supported_files(directory)

    workers = config.current.get("max_threads")
    if not workers:
        for file in file_list:
            console.print_debug(DEBUG_ALL, f"Working on a file: `{file}`")

            convert_handler([file])
    else:
        futures = []

        # starting new thread for each small file is waste of time, so instead create list of files to be converted for
        # each thread that will be started
        job_list = group_elements(file_list, workers)

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            for i, job in enumerate(job_list):
                future = executor.submit(convert_handler, job, f"[THREAD {i}]:")
                futures.append(future)

        concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)

    console.print_info("Finished converting files")

def main():
    config.read_config()

    # no need to use locks if not using multithreading (saved miliseconds you can spend however you want!)
    if config.current.get("max_threads"):
        console.create_lock()

    console.print_warning("This script may require A LOT of space to unpack everything, up to triple size of the game. "
                          "If it will run out space, behavior is unexpected! Also, this process will take a while to"
                          "even on fast CPUs.")
    console.wait_for_confirmation()

    elex2_dir = dirman.get_dir_from_arg(1)
    console.print_debug(DEBUG_FAST, f"Elex 2 directory: `{elex2_dir}`")

    # target folder is optional so script can be used with drag-and-drop
    target_dir = dirman.get_dir_from_arg(2, required=False)
    if not target_dir:
        target_dir = dirman.get_location(elex2_dir)

    unpacked_dir = prepare_unpacked_folder(target_dir)
    if not unpacked_dir:
        return STATUS_ERROR

    abs_pak_path = get_pak_location(elex2_dir)
    if not abs_pak_path:
        return STATUS_ERROR

    unpack_all_pak(abs_pak_path, unpacked_dir)

    convert_all_to_doc(unpacked_dir)

    console.print_success("It seems everything worked correctly")

    return 0

if __name__ == "__main__":
    start_timer()

    try:
        main()
    except:
        console.print_error("Unhandled exception occured! Script error?\n")
        raise

    console.print_info("Script execution time: {} minutes {} seconds (not counting time spend on removing old files "
                       "or waiting for user input)".format(*calculate_elapsed_time()))

    console.wait_for_confirmation()
