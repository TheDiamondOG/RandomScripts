#!/bin/python3


import os
import json
import time
import random
import argparse
import threading

import requests

from rich.console import Console


console = Console()

parser = argparse.ArgumentParser()

banner = """██╗   ██╗██████╗ ██╗          ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║   ██║██╔══██╗██║         ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██████╔╝██║         ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║   ██║██╔══██╗██║         ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║███████╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝"""

console.print(banner, style="purple")

parser.add_argument("file")
parser.add_argument("-d", "--domains", action="store_true")
parser.add_argument("-t", "--threads")
parser.add_argument("-de", "--delay")
parser.add_argument("-o", "--output")

args = parser.parse_args()

user_agents = requests.get("https://raw.githubusercontent.com/cvandeplas/pystemon/refs/heads/master/user-agents.txt").text.strip().splitlines()

if args.threads:
    max_threads = int(args.threads)
else:
    max_threads = 50

if args.delay:
    delay = float(args.delay)
else:
    delay = 0.01

working_urls = []
timed_out_urls = []

url_list = []

threads = []

def check_url():
    url = url_list[0]

    url_list.remove(url)

    url = url.strip()
    if not url.replace(" ","").replace("==","") == "" or not url.startswith("Timed Out URLs:") or not url.startswith("Working URLs:"):
        if not url.startswith("https://") and not url.startswith("http://"):
            url = "https://" + url
            try:
                console.print(f"Testing URL: {url}", style="cyan")
                res = requests.get(url, headers={"User-Agent": random.choice(user_agents)}, timeout=10)
                            
                if args.domains == False:
                    if res.status_code != 404:
                        console.print(f"Real URL: {url}", style="green")
                        working_urls.append(url)
                    else:
                        console.print(f"Fake URL: {url}", style="red")
                else:
                    console.print(f"Real URL: {url}", style="green")
                    working_urls.append(url)
            except requests.exceptions.Timeout:
                console.print(f"Timed Out: {url}", style="cyan")
                timed_out_urls.append(url)
            except Exception as e:
                console.print(f"Fake URL: {url}", style="red")
                pass


if args.file:
    if os.path.exists(args.file):
        if os.path.isfile(args.file):
            with open(args.file, "r") as f:
                url_list = f.readlines()

                for url in url_list:
                    while True:
                        if len(threads) < max_threads:
                            console.print(f"Starting thread for {url}", style="cyan")

                            thread = threading.Thread(target=check_url)

                            thread.start()

                            threads.append(thread)

                            break
                        else:
                            console.print("Max Threads Hit", style="red")
                            for thread in threads:
                                thread.join()
            console.print("Finished Starting Threads", style="red")
            for thread in threads:
                thread.join()
            console.print("Finished", style="green")
        else:
            console.print("That is not a file", style="cyan")
    else:
        console.print("File does not exist", style="red")

if args.output:
    with open(args.output, "w+") as f:
        if args.output.endswith(".json"):
            data = {
                "working": working_urls,
                "timed": timed_out_urls
            }

            json.dump(data, f)
        else:
            f.write("Working URLs:\n")
            f.write('\n'.join(working_urls))
            f.write("\n=======================================\n\n")

            f.write("Timed Out URLs:\n")
            f.write('\n'.join(timed_out_urls))

        console.print(f"Wrote output to {args.output}", style="cyan")
