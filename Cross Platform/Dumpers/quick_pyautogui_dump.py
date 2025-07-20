import pyautogui

with open("keys.txt", "w+") as f:
    f.write('\n'.join(pyautogui.KEY_NAMES))