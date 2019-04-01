# Daniel McGinn
# Run with python3
# Serves webpage at Router Level
# Add ability to input EV3 IP Address from webserver
# See RasPiEV3HubMap.png

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import getpass
import sys
import telnetlib
import socket

# Initialize global variables
tn = ""
connected = False
speed = "100"

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

        html = '''
            <html>
            <body style="width:960px; margin: 20px auto;">
            <h1>EV3Dev Telnet Webserver Demo on Raspberry Pi</h1>
            <p>EV3 Connection State: {}</p>
            <form action="/IP" method="POST">
            <p>Enter EV3 IP Address to Connect</p>
             <input type="text" name="submit" placeholder="IP Address" id="ev3ip">
             <input type="submit" name="connect" value="connect" onclick="myFunction()">
            </form>
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
            # HTML code to show IP address when connection is pending:
            # Doesn't work when writting variables with self.wfile.write(html.format(connected).encode("utf-8"))
            # becasue curly brackets are misinterpreted

            # <p id="DispEV3IP"></p>
            # <script>
            # function myFunction() {
            #   var ip = document.getElementById("ev3ip").value;
            #   var str = "Connecting to EV3 at "
            #   var str2 = str.concat(ip);
            #   document.getElementById("DispEV3IP").innerHTML = str2;
            # }
            # </script>

        self.do_HEAD()
        self.wfile.write(html.format(connected).encode("utf-8"))
        return connected

    def do_POST(self):
        global tn
        global connected
        global speed

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        print(post_data) # Uncomment for debugging

        if 'connect' in post_data and connected == False:
            post_data_ip = post_data.split("&")[0]
            tn = telnetlib.Telnet(post_data_ip)
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
            # print("Connected - %s" % (connected)) # Uncomment for debugging
            # print("post_data_ip - %s" % (post_data_ip)) # Uncomment for debugging
            # print("tn - %s" % (tn)) # Uncomment for debugging
        elif post_data == 'Red':
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
            tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
        elif post_data == 'Forward':
            tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
        elif post_data == 'Right':
            tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
        elif post_data == 'Backward':
            tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
        elif post_data == 'Stop':
            tn.write("motor_left.run_direct(duty_cycle_sp=0);motor_right.run_direct(duty_cycle_sp=0)\n".encode('utf-8'))
        self._redirect('/')  # Redirect back to the root url
        
        return tn
        return connected
        return speed

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
    print("Server Starts - %s:%s" % (ip_address, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
