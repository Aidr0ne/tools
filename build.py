#! usr/bin/python

import argparse
import os
import sys
import shutil

parser = argparse.ArgumentParser(description='Builds into a single folder')                                # Implement the building part
parser.add_argument('-s', '--source', required=True, help='Source directory')                              # Implement This
parser.add_argument('-o', '--output', required=True, help='Output directory')                              # Implement This
parser.add_argument('-c', '--clean', action='store_true', help='Clean output directory before building')   # Done
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')                         # To Be Done throughout the build
parser.add_argument('-q', '--quiet', action='store_true', help='Quiet output')
parser.add_argument('-t', '--type', choices=['debug', 'release'], default='release', help='Build type')    # Part of build
parser.add_argument('-f', '--config', help='Configuration file')                                           # Implement This
parser.add_argument('--version', action='version', version='Build Tool 0.1')                               # Well very easy i guess
parser.add_argument('--no-confirm-deletion', action='store_true', help='Do not confirm deletion of files') # Done
parser.add_argument('--test-mode', action='store_true', help='Test mode')                                  #
                                                                                                           # TODO: IMPLEMENT ABOVE ITEMS

args = parser.parse_args()
if args.clean:
    rem_list = [
        '__pycache__',
        '.mypy_cache',
        'docs',
        '.vscode',
        '.git',
        '.gitignore',
        '.gitattributes',
    ]

    found_list = []

    source = args.source
    for dirpath, dirnames, filenames in os.walk(source, topdown=False):
        # Delete matching files
        for file in filenames:
            if file in rem_list:
                file_path = os.path.join(dirpath, file)
                found_list.append(["File:", file_path])

    for dir in dirnames:
        if dir in rem_list:
            dir_path = os.path.join(dirpath, dir)
            found_list.append(["Dir: ", dir_path])

    def delete_items(found_list):
        for item in found_list:
                if not args.test_mode:
                    if item[0] == "File":
                        os.remove(item[1])
                    else:
                        shutil.rmtree(item[1])
                if args.verbose:
                    print(f"Deleted: {item[0]}: {item[1]}")

    print("Found Items: ")
    for item in found_list:
        print(f"{item[0]}{item[1]}, ")
    if not args.no_confirm_deletion:
        i = input("Delete? (y/n): ")
        if i == "y":
            delete_items(found_list)
    else:
        delete_items(found_list)
            
             


