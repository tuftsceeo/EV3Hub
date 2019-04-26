# Daniel McGinn
# Run with python3
# Terminal With Ripple Window Hosted on Webpage
# See TerminalWebserver.png

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, telnetlib, socket, os, webbrowser

# Initialize global variables
tn = ""
connected = False
post_data_ip = "0"
terminal = "" #intialize blank terminal

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

# Set host port
host_port = 8000

# Webserver
class MyServer(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        global connected
        global post_data_ip
        global terminal

        if connected == True:
            status = "You are connected to an EV3 with IP Address "+post_data_ip
        else:
            status = "Enter your EV3s IP Address and click connect"

        self.do_HEAD()
        self.wfile.write(open('TerminalSite.html').read().format(status, terminal).encode("utf-8"))
        return connected
        return post_data_ip
        return terminal

    def do_POST(self):
        global tn
        global post_data_ip
        global connected
        global terminal

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
#        print(post_data) # Uncomment for debugging

        if 'Connect' in post_data and connected == False:
            post_data_ip = post_data.split("&")[0]
            tn = telnetlib.Telnet(post_data_ip)
            tn.read_until("login: ".encode('utf-8')).decode('utf-8')
            tn.write("robot\n".encode('utf-8'))
            tn.read_until("Password: ".encode('utf-8')).decode('utf-8')
            tn.write("maker\n".encode('utf-8'))
            #Take out ASCII ev3dev logo becuase it doesn't look right in the textbox
            terminal = "Debian"+tn.read_until("robot@ev3dev:~$".encode('utf-8')).decode('utf-8').split("Debian")[1] 
            tn.write("python3\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            tn.write("import ev3dev.ev3 as ev3\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            print("-----------Connection Initiated-----------")
            connected = True
        elif 'SendCommand' in post_data:
            command = post_data.split("&")[0]
            command = command.replace("+", " ")
            command = unquote(command)
            count = terminal.count("robot")
            print(count)
            if count > 1:
                command =command.split(">>> |robot@ev3dev:~$ ")[-1] #Allow the ability to exit python
            else:
                command =command.split(">>> ")[-1]
            tn.write((command+"\n").encode('utf-8'))
            tup = tn.expect(["robot ".encode('utf-8'),">>> ".encode('utf-8')],timeout=None)
            print("tup2 - %s" % (tup[2]))
            terminal = terminal+tup[2].decode('utf-8')
        self._redirect('/')  # Redirect back to the root url
        
        return tn
        return post_data_ip
        return connected
        return terminal

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
