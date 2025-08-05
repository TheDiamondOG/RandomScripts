import os
import random
import time
import atexit

 # Originally from https://github.com/TheDiamondOG/Hacker-Binary-Script

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

colors = bcolors()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

character_list = ["~", "`", "1", "!", "2", "@", "3", "#", "4", "$", "5", "%", "6", "^", "7", "&", "8", "*", "9", "(", "0", ")", "-", "_", "=", "+", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "{", "]", "}", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", ":", "'", '"', "\\", "|", "z", "x", "c", "v", "b", "n", "m", ",", "<", ".", ">", "/", "?"]

def true_false():
    tfl = [True, False]
    return random.choice(tfl)

def random_character(random_case:bool=False):
    character = random.choice(character_list)
    if random_case == True:
        rand_case = true_false()
        if rand_case == True:
            character = character.upper()
        if rand_case == False:
            character = character.lower()
    return character

clear()

calabration = len(input(f"{colors.OKCYAN}Put as many 0 as it needs to make a line across your screen\n"))

while True:

    try:

        print(colors.OKCYAN)

        print("Please set a delay for the loop, I recommend either 0.01 or 0.001")

        delay = float(input("Delay: "))

        break
    except Exception:

        print(f"{colors.FAIL}It needs to be a number{colors.ENDC}")

while True:

    try:

        print(colors.OKCYAN)

        print("Choose a number higher than 1 to get spaces or choose 1 to get no spaces.\nI recommend setting this to 5.")

        space_number = int(input("Chance of space: ")) +1

        break

    except Exception:

        print(f"{colors.FAIL}It needs to be a number{colors.ENDC}")

print(colors.OKCYAN)

print("Do you want to use random characters?")

random_character_choice = input("Characters (y/N): ")

if random_character_choice.lower() == "y":
    random_character_choice = True

    print("Do you want to use random casing?")

    random_case = input("Random Casing (Y/n): ")
    if random_case.lower() == "y" or random_case.replace(" ", ""):
        random_case = True
    else:
        random_case = False
else:
    random_character_choice = False

if space_number <= 0:

    space_number = 1

print(colors.ENDC)

number_list = []

atexit.register(clear)

clear()

while True:

    for i in range(calabration):

        if random_character_choice == True:

            rand_stuff = random.randint(0, space_number)

            if rand_stuff >= 2:
                rand_stuff = " "
            else:
                rand_stuff = random_character(random_case)

        else:

            rand_stuff = random.randint(0, space_number)

            if rand_stuff >= 2:
                rand_stuff = " "

        number_list.append(str(rand_stuff))

    number_line = ''.join(number_list)

    print(f"{colors.OKGREEN}{number_line}{colors.ENDC}")

    number_list = []

    time.sleep(delay)
