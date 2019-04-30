# Daniel McGinn
# Run with python3
# Serves webpage at Router Level
# Add ability to input EV3 IP Address from webserver
# See RasPiEV3HubMap.png

# C bug - post_data_ip & tn are defined in an if statement and need to be accessed in other if statements
# Try running that section of the code in def do_GET(self): NOT def do_POST(self):
# make post_data_ip the value of the textbox, so it can be resubmitted each time
# have the server send the ip address each time so that post_data_ip & tn are defined at the begining of each if statement 

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import getpass
import sys
import telnetlib
import socket

x = ""

# Get IP Address
ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0]
s.close()

host_port = 8000


# Create Webserver
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
        global x

        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>EV3Dev Telnet Webserver Demo on Raspberry Pi</h1>
            <form action="/IP" method="POST">
            <p>Enter EV3 IP Address to Connect</p>
             <input type="text" name="submit" placeholder="IP Address" id="ev3ip">
             <button onclick="myFunction()">Connect</button>
            </form>
            <p id="DispEV3IP"></p>

            <script>
            function myFunction() {
              var x = document.getElementById("ev3ip").value;
              document.getElementById("DispEV3IP").innerHTML = x;
            }
            </script>
            <form action="/" method="POST">
            <p>Control EV3 Onboard LEDs</p>
             <input type="submit" name="submit" value="Red">
             <input type="submit" name="submit" value="Orange">
             <input type="submit" name="submit" value="Yellow">
             <input type="submit" name="submit" value="Green">
             <input type="submit" name="submit" value="Off">
            <p>Drive EV3</p>
             <input type="submit" name="submit" value="Left">
             <input type="submit" name="submit" value="Forward">
             <input type="submit" name="submit" value="Right">
             <input type="submit" name="submit" value="Backward">
             <input type="submit" name="submit" value="Stop">
            </form>
            </body>
            </html>
        '''
        self.do_HEAD()
        # Write code here to record IP address from ev3ip
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        global tn

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        print(post_data) # Uncomment for debugging
        print(x)

        if 'Connect' in post_data:
            post_data_ip = post_data.split("&")[0]
            tn = telnetlib.Telnet(post_data_ip)
        else: 
            post_data_ip = "10.0.0.240"
            tn = telnetlib.Telnet(post_data_ip)
        if post_data_ip and 'connected' not in locals():
            tn.read_until("login: ".encode('utf-8'))
            tn.write("robot\n".encode('utf-8'))
            tn.read_until("Password: ".encode('utf-8'))
            tn.write("maker\n".encode('utf-8'))
            tn.read_until("robot@ev3dev:~$".encode('utf-8'))
            tn.write("python3\n".encode('utf-8'))
            tn.read_until(">>>".encode('utf-8'))
            tn.write("import ev3dev.ev3 as ev3\n".encode('utf-8'))
            tn.read_until(">>>".encode('utf-8'))
            tn.write("motor_left = ev3.LargeMotor('outB');motor_right = ev3.LargeMotor('outC')\n".encode('utf-8'))
            tn.read_until(">>>".encode('utf-8'))
            print("-----------Connection Initiated-----------")
            connected = True
            print("Connected - %s" % (connected))
            print("post_data_ip - %s" % (post_data_ip))
            print("tn - %s" % (tn))
        elif post_data == 'Red':
            print("Red Start post_data_ip - %s" % (post_data_ip))
            print("Red Start tn - %s" % (tn))
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)\n".encode('utf-8')) 
            tn.read_until(">>>".encode('utf-8'))
        elif post_data == 'Orange':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)\n".encode('utf-8')) 
            tn.read_until(">>>".encode('utf-8'))
        elif post_data == 'Yellow':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)\n".encode('utf-8')) 
            tn.read_until(">>>".encode('utf-8'))
        elif post_data == 'Green':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)\n".encode('utf-8')) 
            tn.read_until(">>>".encode('utf-8'))
        elif post_data == 'Off':
            tn.write("ev3.Leds.all_off()\n".encode('utf-8'))
        elif post_data == 'Left':
            tn.write("motor_left.run_direct(duty_cycle_sp=-10);motor_right.run_direct(duty_cycle_sp=10)\n".encode('utf-8'))
        elif post_data == 'Forward':
            tn.write("motor_left.run_direct(duty_cycle_sp=10);motor_right.run_direct(duty_cycle_sp=10)\n".encode('utf-8'))
        elif post_data == 'Right':
            tn.write("motor_left.run_direct(duty_cycle_sp=10);motor_right.run_direct(duty_cycle_sp=-10)\n".encode('utf-8'))
        elif post_data == 'Backward':
            tn.write("motor_left.run_direct(duty_cycle_sp=-10);motor_right.run_direct(duty_cycle_sp=-10)\n".encode('utf-8'))
        elif post_data == 'Stop':
            tn.write("motor_left.run_direct(duty_cycle_sp=0);motor_right.run_direct(duty_cycle_sp=0)\n".encode('utf-8'))
        self._redirect('/')  # Redirect back to the root url

if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
