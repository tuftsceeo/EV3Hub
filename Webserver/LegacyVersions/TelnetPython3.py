# Daniel McGinn
# Open a telnet connection from a PC or Mac to an EV3 running on EV3Dev 
# Allows the user to run python commands on the EV3
# Run with python

import getpass
import sys
import telnetlib

HOST = raw_input("Enter EV3 IP Address: ")
tn = telnetlib.Telnet(HOST)

tn.read_until("login: ")
tn.write("robot\n")
tn.read_until("Password: ")
tn.write("maker\n")


print tn.read_until("robot@ev3dev:~$")
tn.write("python3\n")
command = "TBD" #Initiate command to start the loop
while command != "quit()":
   print tn.read_until(">>>")
   command = raw_input("Enter Command: ")
   tn.write(command  + "\n")
#print tn.read_until(">>>")