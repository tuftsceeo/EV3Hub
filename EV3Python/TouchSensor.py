#!/usr/bin/env python3
# so that script can be run from Brickman

from ev3dev.ev3 import *

# Connect touch sensors to any sensor ports
ts = TouchSensor()
while 1:
	if ts.value():
		Leds.set_color(Leds.LEFT, Leds.GREEN);Leds.set_color(Leds.RIGHT, Leds.GREEN)
		Sound.beep()  
	else:
		Leds.set_color(Leds.LEFT, Leds.RED);Leds.set_color(Leds.RIGHT, Leds.RED)