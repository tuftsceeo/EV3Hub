# Daniel McGinn
# Open a telnet connection from a PC or Mac to an EV3 running on EV3Dev

import getpass
import sys
import telnetlib

HOST = raw_input("Enter EV3 IP Address: ")
tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write("robot\n")
tn.read_until("Password: ")
tn.write("maker\n")

n = 1
while n == 1:
   print tn.read_until("robot@ev3dev:")
   command = raw_input("Enter Command: ")
   tn.write(command  + "\n")
   if command == "exit":
      n = 0
print tn.read_all()