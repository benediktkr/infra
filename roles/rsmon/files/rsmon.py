#!/usr/bin/env python3.7

from glob import glob
import subprocess
import os

from blink1.blink1 import Blink1

def clear_light():
    b1 = Blink1()
    b1.fade_to_color(200, (0, 0, 0))

def set_color(color):
    b1 = Blink1()
    b1.fade_to_color(200, color)

def tests(color):
    tests = glob(os.path.join("/srv/rsmon", color, "*"))
    print(tests)
    triggered = False

    for test in tests:
        res = subprocess.call([test])
        if res != 0:
            triggered = True

    return triggered


if __name__ == "__main__":
    clear = True
    for color in ['yellow', 'pink', 'red']:
        print(color)
        triggered = tests(color)
        clear = not triggered
        if triggered:
            set_color(color)
    if clear:
        clear_light()
