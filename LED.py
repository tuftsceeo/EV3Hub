# Dan McGinn
# Keyboard inputs adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
# Run with python3

from ev3dev.ev3 import *
from time import sleep
import termios,tty,sys

# Initiate keybaord inputs
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def red():
    Leds.set_color(Leds.LEFT,  Leds.RED)
    sleep(0.01)
    Leds.set_color(Leds.RIGHT, Leds.RED)
    sleep(0.01)
def orange():
    Leds.set_color(Leds.LEFT,  Leds.ORANGE)
    sleep(0.01)
    Leds.set_color(Leds.RIGHT, Leds.ORANGE)
    sleep(0.01)
def yellow():
    Leds.set_color(Leds.LEFT,  Leds.YELLOW)
    sleep(0.01)
    Leds.set_color(Leds.RIGHT, Leds.YELLOW)
    sleep(0.01)
def green():
    Leds.set_color(Leds.LEFT,  Leds.GREEN)
    sleep(0.01)
    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    sleep(0.01)

print("Connection Initiated")
while True:
   char = getch()
   if char == 'r':
      red()
      print("Red")
   if char == 'o':
      orange()
      print("Orange")
   if char == 'y':
      yellow()
      print("Yellow")
   if char == 'g':
      green()
      print("Green")
   if char == 'q':
      Leds.all_off()
      exit()