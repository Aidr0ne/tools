#! /usr/bin/python

import argparse


"""
Builds the game into build

Args: --use-common-location [true]
      --name [str]
      --add-dependencies [true]

"""

parser = argparse.ArgumentParser(
    prog="Build Utility",
    description="Utility to package files into a build folder"
)

parser.add_argument("-n", "--name")
parser.add_argument("--use-common-location", action="store_true")
parser.add_argument("--add-dependencies", action="store_true")

args = parser.parse_args()

if args.add_dependencies:
    pass #TODO: Implement

if args.use_common_location:
    pass