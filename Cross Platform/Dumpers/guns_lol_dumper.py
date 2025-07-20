import os
import json
import shutil
import argparse
from datetime import datetime

import cloudscraper
from bs4 import BeautifulSoup
from rich.console import Console

scraper = cloudscraper.create_scraper()

console = Console()

parser = argparse.ArgumentParser()

parser.add_argument("username")
parser.add_argument("-o", "--output")

args = parser.parse_args()

username = args.username

def clear():
    os.system("clear")

def pause():
    console.print("Enter to continue...", style="cyan")
    input()

def dumper():
    banner = """     ██████╗ ██╗   ██╗███╗   ██╗███████╗   ██╗      ██████╗ ██╗         ██████╗ ██╗   ██╗███╗   ███╗██████╗ ███████╗██████╗ 
    ██╔════╝ ██║   ██║████╗  ██║██╔════╝   ██║     ██╔═══██╗██║         ██╔══██╗██║   ██║████╗ ████║██╔══██╗██╔════╝██╔══██╗
    ██║  ███╗██║   ██║██╔██╗ ██║███████╗   ██║     ██║   ██║██║         ██║  ██║██║   ██║██╔████╔██║██████╔╝█████╗  ██████╔╝
    ██║   ██║██║   ██║██║╚██╗██║╚════██║   ██║     ██║   ██║██║         ██║  ██║██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══╝  ██╔══██╗
    ╚██████╔╝╚██████╔╝██║ ╚████║███████║██╗███████╗╚██████╔╝███████╗    ██████╔╝╚██████╔╝██║ ╚═╝ ██║██║     ███████╗██║  ██║
     ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝╚══════╝ ╚═════╝ ╚══════╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝"""

    if args.output:
        export_path = args.output
    else:
        export_path = os.getcwd()+"/exports/guns.lol dumper/"+username

    console.print("Getting guns.lol page", style="cyan")
    res = scraper.get(f"https://guns.lol/{username}")

    console.print("Starting the parser", style="cyan")
    soup = BeautifulSoup(res.content, 'html.parser')

    console.print("Checking to see if the user exists", style="cyan")
    h1_tags = soup.find_all("h1")

    for h1 in h1_tags:
        if "This user is not claimed" in h1.text:
            console.print("User does not exist", style="red")
            pause()
            return

    console.print("Getting All Scripts", style="cyan")
    script_tags = soup.find_all("script")

    user_data = {}

    for script in script_tags:
        script_text = script.text.strip()

        if "account_created" in script_text:
            script_text = script_text.split(',null,')[-1]
            script_text = script_text.replace(']\\n"])', "")
            script_text = script_text.replace('])', "}}}}")
            script_text = script_text.replace('\\"', '"')
            script_text = script_text.replace(',"button_border_ra"', "")

            try:
                user_data = json.loads(script_text)["data"]

                #console.print(script_text)

                break
            except Exception as e:
                console.print("Failed to format user data...", style="red")
                console.print(e, style="red")
                console.print(script_text)

                return

    dumped_data = {
        "links": [],
        "audio": [],
        "avatar": "",
        "background": "",
        "cursor": "",
    }

    console.print("Grabbing Profile Links", style="cyan")
    for link in user_data["config"]["socials"]:
        dumped_data["links"].append(link["value"])

    console.print("Grabbing Profile Audio", style="cyan")
    for audio in user_data["config"]["audio"]:
        dumped_data["audio"].append({"name": audio["title"], "url": audio["url"]})

    console.print("Grabbing Profile Picture", style="cyan")
    dumped_data["avatar"] = user_data["config"]["avatar"]

    console.print("Grabbing Background Picture", style="cyan")
    dumped_data["background"] = user_data["config"]["url"]

    if "\\" in os.getcwd():
        slasher = "\\"
    else:
        slasher = "/"

    console.print("Dumping found data to " + os.getcwd() + slasher + export_path, style="cyan")

    if os.path.exists(export_path):
        shutil.rmtree(export_path)

    os.makedirs(export_path, exist_ok=True)

    console.print("Dumping links", style="cyan")
    with open(export_path + "/links.txt", "w+") as f:
        f.write('\n'.join(dumped_data["links"]))

    console.print("Dumping account data", style="cyan")
    with open(export_path + "/account_data.txt", "w+") as f:
        f.write("Username: " + user_data["username"] + "\n")
        f.write("Display Name: " + user_data["config"]["display_name"] + "\n")
        if user_data.get("uid"):
            f.write("User ID: " + str(user_data["uid"]) + "\n")
        f.write("Alias: " + user_data["alias"] + "\n")
        f.write("Account Creation: " + datetime.fromtimestamp(user_data["account_created"]).strftime(
            "%b %d, %Y %H:%M:%S") + "\n")

        if user_data["config"].get("location"):
            if user_data["config"]["location"] != "":
                f.write("Stated Location: " + user_data["config"]["location"] + "\n")
        f.write("Badges:" + "\n")
        for badge in user_data["config"]["user_badges"]:
            f.write(badge["name"] + "\n")
        if user_data.get("premium"):
            f.write("Premium: " + str(user_data["premium"]) + "\n")
        if user_data.get("discord"):
            f.write("Discord Username: " + user_data["discord"]["username"] + "\n")
            f.write("Discord ID: " + user_data["discord"]["id"] + "\n")
            f.write("Discord URL: https://discord.com/users/" + user_data["discord"]["id"] + "\n")

    os.mkdir(export_path + "/images")

    if dumped_data["avatar"] != "":
        console.print("Dumping profile picture", style="cyan")
        with open(export_path + f"/images/profile.{dumped_data["avatar"].split('.')[-1]}", "wb") as f:
            res = scraper.get(dumped_data["avatar"])

            f.write(res.content)

    if dumped_data["background"] != "":
        console.print("Dumping background picture", style="cyan")
        with open(export_path + f"/images/background.{dumped_data["background"].split('.')[-1]}", "wb") as f:
            res = scraper.get(dumped_data["background"])

            f.write(res.content)

    if dumped_data["audio"] != []:
        console.print("Dumping audio", style="cyan")
        os.mkdir(export_path + "/audio")
        for audio in dumped_data["audio"]:
            with open(export_path + f"/audio/{audio['name']}.{audio['url'].split('.')[-1]}", "wb") as f:
                res = scraper.get(audio['url'])

                f.write(res.content)

    with open(export_path + f"/raw_data.json", "w+") as f:
        json.dump(user_data, f, indent=4)

    console.print("Finished dumping data", style="cyan")
    pause()

dumper()