import pyautogui
import string
import random
import time

delay_float_list = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

repeat_times = random.randint(1,10)

input("Enter to start the countdown...\n")

start_delay = 5

print(f"Keyboard smashing in {start_delay} seconds")

for i in range(start_delay):
    print(start_delay-i)
    time.sleep(1)

for i in range(repeat_times):
    random_characters = random.choices(string.ascii_letters+"1234567890", k=random.randint(10, 25))

    print(f"Typing "+"".join(random_characters))

    open_chat = ["t", "backspace"]

    pyautogui.press(open_chat)
    pyautogui.press(random_characters)
    pyautogui.press("enter")
    time.sleep(random.choice(delay_float_list))