import pyautogui
import time

input("Enter to start the countdown...\n")

start_delay = 5

print(f"Holding W in {start_delay} seconds")

for i in range(start_delay):
    print(start_delay-i)
    time.sleep(1)

print("Get moving")
pyautogui.keyUp("w")
pyautogui.keyDown("w")