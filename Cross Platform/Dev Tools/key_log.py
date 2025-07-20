from pynput import keyboard

def on_press(key):
    try:
        print(key.char)
    except AttributeError:
        print(f"SP: {key}")

def on_release(key):
    if key == keyboard.Key.esc:
        print("Exiting...")
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
