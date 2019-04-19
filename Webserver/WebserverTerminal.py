# Daniel McGinn
# Run with python3
# Terminal Hosted on Webpage
# See TerminalWebserver.png

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import getpass, sys, telnetlib, socket, os

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

        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <aside bgcolor="#FFFFFF" style="float:right;width:400px;">
              <h3><br><br>Example Code</h3>
              <p style="color:red;">Turn Left Onboard LED Red: ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)<br>Turn Right Onboard LED Red: ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)</p>
              <p style="color:orange;">Turn Left Onboard LED Orange: ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)<br>Turn Right Onboard LED Orange: ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE</p>
              <p style="color:#B9B538;">Turn Left Onboard LED Yellow: ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)<br>Turn Right Onboard LED Yellow: ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)</p>
              <p style="color:green;">Turn Left Onboard LED Green: ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)<br>Turn Right Onboard LED Green: ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)</p>
            </aside>
            <h1>EV3 Terminal Window</h1>
            <form action="/IP" method="POST">
            <p>{}</p>
             <input type="text" name="submit" placeholder="IP Address" id="ev3ip">
             <input type="submit" name="Connect" value="Connect" onclick="myFunction()">
            </form>
            <form action="/" method="POST">
             <input type="text" name="submit" placeholder="Enter Python3 Command" id="command" size="65">
             <input type="submit" name="SendCommand" value="Send Command">
            </form>
            <textarea rows="21" cols="80">{}</textarea>
            </body>
            </html>
        '''

        self.do_HEAD()
        self.wfile.write(html.format(status, terminal).encode("utf-8"))
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
        print(post_data) # Uncomment for debugging

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
            terminal = terminal+tn.read_until(">>>".encode('utf-8')).decode('utf-8')
            tn.write("import ev3dev.ev3 as ev3\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>>".encode('utf-8')).decode('utf-8')
            print("-----------Connection Initiated-----------")
            connected = True
        elif 'SendCommand' in post_data:
            command = post_data.split("&")[0]
            #Some UTF8 characters still remain even after decoding, so I have to replace them manually
            command = command.replace("+", " ").replace("%28","(").replace("%29",")").replace("%2C",",").replace("%3B",";").replace("%2B","+")
            print(command)
            tn.write((command+"\n").encode('utf-8'))
            terminal = terminal+tn.read_until(">>>".encode('utf-8')).decode('utf-8')
        self._redirect('/')  # Redirect back to the root url
        
        return tn
        return post_data_ip
        return connected
        return terminal

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
