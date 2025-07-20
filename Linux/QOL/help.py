#!/bin/python3

import os
import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output")
parser.add_argument("-nl", "--new_line", action="store_true")

args = parser.parse_args()

bin_path = os.listdir("/bin")
sbin_path = os.listdir("/sbin")
usr_bin_path = os.listdir("/usr/bin")
    
command_list = []
root_only_list = []

for command in bin_path:
    if not command in command_list:
        command_list.append(command)
        
for command in usr_bin_path:
    if not command in command_list:
        command_list.append(command)
        
for command in sbin_path:
    if not command in command_list:
        root_only_list.append(command)

if args.new_line:
    text = """Command list:
"""+',\n'.join(command_list)+"""

===============================================================

Root only command list:
"""+',\n'.join(root_only_list)
else:
    text = f"""Command list:
"""+', '.join(command_list)+"""

===============================================================

Root only command list:
"""+', '.join(root_only_list)

data = {
    "normal": command_list,
    "root": root_only_list
}

if args.output:
    with open(args.output, "w+") as f:
        if args.output.endswith(".json"):
            if args.new_line:
                json.dump(data, f, indent=4)
            else:
                json.dump(data, f)
        else:
            f.write(text)
else:
    print(text)
