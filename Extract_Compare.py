#!/usr/bin/env python3

import os
from pathlib import Path
import subprocess
import hashlib
import shutil

# Constants
MD5_HASH_FILES = True

ORIGINAL_DIR = "./Original Game Files"
NEW_DIR = "./New Game Files"
WAV_DIR = "./WAV"

TOOLS_DIR = "./Tools"
ORIGINAL_DECODE_DIR = "./Tools/Original Decoding"
NEW_DECODE_DIR = "./Tools/New Decoding"

# Check if running on Windows and append .exe if so
EXECUTABLE_EXTENSION = ""
if os.name == 'nt':
    EXECUTABLE_EXTENSION = ".exe"

# Function to clean directories
def cleanup_dirs(*dirs):
    for dir in dirs:
        dir_path = Path(dir)
        if dir_path.exists():
            shutil.rmtree(dir_path)  # Remove directory and all its contents
        dir_path.mkdir(parents=True, exist_ok=True)  # Recreate the directory

# Extract individual audio files from Wwise PCK files with quickbms
def extract_files(original_dir, output_dir):
    tools_dir_abs = Path(TOOLS_DIR).resolve()
    subprocess.call([Path.joinpath(tools_dir_abs, "quickbms" + EXECUTABLE_EXTENSION), Path.joinpath(tools_dir_abs, "wavescan.bms"), Path(original_dir).resolve(), Path(output_dir).resolve()])

# Find and return list of all files in new_dir that are not also present in original_dir
def filter_diff_files(original_dir, new_dir):
    original_dir_abs = Path(original_dir).resolve()
    new_dir_abs = Path(new_dir).resolve()
    # Calculate list of new files
    original_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(original_dir):
        original_file_list.extend(filenames)
        break
    original_file_list = list(filter(lambda name: Path(name).suffix == ".wem", original_file_list))
    
    new_file_list = []
    for (dirpath, dirnames, filenames) in os.walk(new_dir):
        new_file_list.extend(filenames)
        break
    new_file_list = list(filter(lambda name: Path(name).suffix == ".wem", new_file_list))
    
    return_list = []
    iteration = 0
    if MD5_HASH_FILES:
        total = len(original_file_list) + len(new_file_list)
        old_file_hashes = {}
        new_file_hashes = {}
        # Take MD5 hashes of both new and old music files
        for file_name in original_file_list:
            iteration += 1
            show_progress(iteration, total, "", "Filtering New Files")
            old_file = Path.joinpath(original_dir_abs, file_name)
            file_hash = get_md5(old_file)
            if file_hash:
                old_file_hashes[file_hash + "," + str(old_file.stat().st_size)] = file_name
        for file_name in new_file_list:
            iteration += 1
            show_progress(iteration, total, "", "Filtering New Files")
            new_file = Path.joinpath(new_dir_abs, file_name)
            file_hash = get_md5(new_file)
            if file_hash:
                new_file_hashes[file_hash + "," + str(new_file.stat().st_size)] = file_name
            else:
                return_list.append(file_name)
        # Take the difference, keeping only new file hashes
        diff_keys = set(new_file_hashes.keys()) - set(old_file_hashes.keys())
        total = len(diff_keys)
        iteration = 0
        # Iterate over all new file hashes to get the file names associated with them
        for key in diff_keys:
            iteration += 1
            show_progress(iteration, total, "", "Finalizing")
            return_list.append(new_file_hashes[key])
    else:
        total = len(new_file_list)
        # Iterate over all patched files to find ones that weren't present before
        for file_name in new_file_list:
            iteration += 1
            show_progress(iteration, total, "", "Filtering New Files")
            old_file = Path.joinpath(original_dir_abs, file_name)
            new_file = Path.joinpath(new_dir_abs, file_name)
            # If file name existed in old directory, check sizes
            if old_file.exists():
                old_file_size = old_file.stat().st_size
                new_file_size = new_file.stat().st_size
                if old_file_size != new_file_size:
                    return_list.append(file_name)
            # If file didn't exist in old directory, add to new list
            else:
                return_list.append(file_name)
    return return_list

def get_md5(file):
    try:
        return hashlib.md5(file.read_bytes()).hexdigest()
    except:
        return False

# Convert all files from file_dir with names in file_list to WAV format
def convert_to_wav(file_dir, file_list, output_dir):
    total = len(file_list)
    iteration = 0
    vgmstream_exec = Path.joinpath(Path(TOOLS_DIR).resolve(), "vgmstream-cli" + EXECUTABLE_EXTENSION)
    file_dir_abs = Path(file_dir).resolve()
    output_dir_abs = Path(output_dir).resolve()
    for file_name in file_list:
        iteration += 1
        show_progress(iteration, total, "", "Converting to WAV")
        file = Path.joinpath(file_dir_abs, file_name)
        output_file = Path.joinpath(output_dir_abs, file.stem + ".wav")
        file_hash = get_md5(file)
        if file_hash:
            output_file = Path.joinpath(output_dir_abs, file_hash + ".wav")
        subprocess.call([vgmstream_exec, "-o", output_file, file])

def show_progress(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def main():
    # Clean up decoding directories before starting
    cleanup_dirs(ORIGINAL_DECODE_DIR, NEW_DECODE_DIR)
    
    # Extract all original and new audio files
    extract_files(ORIGINAL_DIR, ORIGINAL_DECODE_DIR)
    extract_files(NEW_DIR, NEW_DECODE_DIR)
    
    # Find any new or changed audio files
    new_file_list = filter_diff_files(ORIGINAL_DECODE_DIR, NEW_DECODE_DIR)
    
    # Convert all new or changed files to WAV format
    convert_to_wav(NEW_DECODE_DIR, new_file_list, WAV_DIR)
    
    # Clean up decoding directories after processing
    cleanup_dirs(ORIGINAL_DECODE_DIR, NEW_DECODE_DIR)

if __name__ == "__main__":
    main()
