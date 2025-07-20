#!/bin/python3

import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-k", "--key")

args = parser.parse_args()

if args.key:
    var_env = os.getenv(args.key)

    print(f"{args.key}: {var_env}")
else:
    env_vars = os.environ

    for key, var in env_vars.items():
        print(f"{key}: {var}")
