# Python script to serve a webpage to control an EV3 running ev3dev via telnet
## Designed by Daniel McGinn in Spring 2019 at Tufts University as part of a Master's Project

Used to control an EV3 running on <a href="https://www.ev3dev.org/">ev3dev</a>, a Debian Linux-based operating system

Webserver code adapted from <a href="https://github.com/e-tinkers/simple_httpserver/blob/master/simple_webserver.py">simple_webserver.py</a>, a python script used to create a webserve from a Raspberry Pi to control GPIO Pins

Useful resource for <a href="https://www.pythonforbeginners.com/code-snippets-source-code/python-using-telnet
">using telnet in python </a>

To install telnet on the EV3:
1. Updates the package list 
```
sudo apt-get update
```
2. Install Telnet package
```
sudo apt-get install telnetd
```

To connect to the EV3 via telnet on a mac:
1. Use Homebrew to install telnet (It does not come preinstalled)
```
brew install telnet
```
2. Connect with Telnet
```
telnet -l robot <ip address>
Password: maker
```