from pynput.keyboard import Key, Controller
from time import sleep

def Space():
    keyboard = Controller()
    keyboard.press(Key.space)
    print("Space pressed")
    keyboard.release(Key.space)
    print("Space released")
