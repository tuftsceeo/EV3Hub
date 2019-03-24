# Daniel McGinn
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import getpass
import sys
import telnetlib
import socket

# Establish Telnet Connection to EV3
HOST = input("Enter EV3 IP Address: ")
tn = telnetlib.Telnet(HOST)
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

host_name = socket.gethostbyname(socket.gethostname()) # local IP adress of your computer
# host_name = '10.0.0.173'  # Hardcode your IP address
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

        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1>EV3Dev Telnet Webserver Demo</h1>
           <p>Control EV3 Onboard LEDs</p>
           <form action="/" method="POST">
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
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value

        if post_data == 'Red':
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
        print(post_data) # Uncomment for debugging 
        self._redirect('/')  # Redirect back to the root url

if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")