import os
import time
import shutil
import argparse

import cloudscraper

from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

parser = argparse.ArgumentParser()

parser.add_argument("url")
parser.add_argument("-o", "--output")

args = parser.parse_args()

scraper = cloudscraper.create_scraper()

res = scraper.get(args.url, allow_redirects=True)

soup = BeautifulSoup(res.content, "html.parser")

if args.output:
    output = args.output
else:
    output = os.getcwd()

os.makedirs(output, exist_ok=True)

with open(output+"/original.html", "w+") as f:
    f.write(res.text)

tag_count = {

}

tags = soup.find_all()

for tag in tags:
    tag_count[tag.name] = 0

for tag in tags:
    tag_count[tag.name] = tag_count[tag.name]+1

    dirm = output+"/"+tag.name

    os.makedirs(dirm, exist_ok=True)

    with open(dirm+"/"+str(tag_count[tag.name])+".html", "w+") as f:
        f.write(str(tag))