# Dan McGinn
# Keyboard inputs adapted from https://github.com/recantha/EduKit3-RC-Keyboard/blob/master/rc_keyboard.py
# EV3 Project: http://inspiredtoeducate.net/inspiredtoeducate/programming-lego-mindstorms-ev3-with-python/
# Run with python3

import time,termios,tty,sys
import ev3dev.ev3 as ev3
from time import sleep

# Define motor outputs
motor_left = ev3.LargeMotor('outB')
motor_right = ev3.LargeMotor('outC')
speed = 80 # Set Speed

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

def forward():
   motor_left.run_direct(duty_cycle_sp=speed)
   motor_right.run_direct(duty_cycle_sp=speed)
def back():
   motor_left.run_direct(duty_cycle_sp=-speed)
   motor_right.run_direct(duty_cycle_sp=-speed)
def left():
   motor_left.run_direct( duty_cycle_sp=-speed)
   motor_right.run_direct( duty_cycle_sp=speed)
def right():
   motor_left.run_direct( duty_cycle_sp=speed)
   motor_right.run_direct( duty_cycle_sp=-speed)
def stop():
   motor_left.run_direct( duty_cycle_sp=0)
   motor_right.run_direct( duty_cycle_sp=-0)
def red():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
    sleep(0.01)
def orange():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
    sleep(0.01)
def yellow():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
    sleep(0.01)
def green():
    ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
    sleep(0.01)
    ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
    sleep(0.01)

print("-----------Connection Initiated-----------")
while True:
   char = getch()
   if char == 'w':
      forward()
      print("Forward")
   if char == 's':
      back()
      print("Backward")
   if char == 'a':
      left()
      print("Left")
   if char == 'd':
      right()
      print("Right")
   if char == ' ':
      stop()
      ev3.Leds.all_off()
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
      print("-------------------EXIT-------------------")
      sleep(0.01)
      stop()
      ev3.Leds.all_off()
      exit()