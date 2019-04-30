# Daniel McGinn
# Run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import getpass, sys, telnetlib, socket, os, webbrowser, ssl

# Initialize global variables
tn = ""
connected = False
post_data_ip = "0"
speed = "50"
drive = "stop"
terminal = "" #intialize blank terminal
page = "simplePage"

pyCode = {'Beep':'''ev3.Sound.beep().wait()'''}

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
        global speed
        global terminal
        global page

#        print('page = ' + page)

        if connected == True:
            status = "You are connected to an EV3 with IP Address "+post_data_ip
        else:
            status = "Enter your EV3s IP Address and click connect"

        

        self.do_HEAD()
        if  (page == 'simplePage'):
            pageContent = (open('WebserverBase.html').read()%(terminal, status))+(open('simple.html').read()%(speed))
        elif (page == 'pythonPage'):
            pageContent = (open('WebserverBase.html').read()%(terminal, status))+(open('python.html').read())
        elif (page == 'formPage'):
            for line in pyCode:
                pageContent = (open('WebserverBase.html').read()%(terminal, status))+(open('form.html').read().format(line,pyCode[line]))

        self.wfile.write(pageContent.encode("utf-8"))

        #self.wfile.write(open('DemoAndTerminal.html').read().format(terminal, status, speed).encode("utf-8"))
        #self.wfile.write((open('WebserverPresentation.html').read()%(terminal, status, speed)).encode("utf-8"))
        return connected
        return post_data_ip
        return speed
        return terminal
        return page

    def do_POST(self):
        global tn
        global post_data_ip
        global connected
        global speed
        global drive
        global terminal
        global page

        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value
        print(post_data) # Uncomment for debugging

        if  'simplePage' in post_data:
            page = 'simplePage'
        elif 'pythonPage' in post_data:
            page = 'pythonPage'
        elif 'formPage' in post_data:
            page = 'formPage'

        if ('Clear' in post_data and terminal != ""):
            print('clearing')
            terminal = '>>> '
        if 'REPL' in post_data:
            command = post_data.split("&")[0]
            command = command.replace("+", " ")
            print("command - %s" % (command))
            tn.write((command+"\n").encode('utf-8'))
            tup = tn.expect(["robot@ev3dev:".encode('utf-8'),">>> ".encode('utf-8')],timeout=None) #Note: dificulty with the ~$ from robot@ev3dev:~$
            print("tup2 - %s" % (tup[2]))
            terminal = terminal+tup[2].decode('utf-8')

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
            tn.write("motor_left = ev3.LargeMotor('outB');motor_right = ev3.LargeMotor('outC')\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            print("-----------Connection Initiated-----------")
            connected = True
        elif 'SendCommand' in post_data:
            command = post_data.split("&")[0]
            command = command.replace("+", " ")
            command = unquote(command).split(">>> ")[-1]
            command = command.rsplit("robot@ev3dev:",1)[-1].rsplit(">>> ",1)[-1] #Allow the ability to exit python
            print("command - %s" % (command))
            tn.write((command+"\n").encode('utf-8'))
            tup = tn.expect(["robot@ev3dev:".encode('utf-8'),">>> ".encode('utf-8')],timeout=None) #Note: dificulty with the ~$ from robot@ev3dev:~$
            print("tup2 - %s" % (tup[2]))
            terminal = terminal+tup[2].decode('utf-8')
        elif 'UpdateSpeed' in post_data:
            speed = post_data.split("&")[0]
            print("Speed set to %s" % (speed)) # Uncomment for debugging
            if drive == 'left': #Resend last drive command with updated speed if it was anything other than "stop"
                tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
                terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            elif drive == 'forward':
                tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
                terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            elif drive == 'right':
                tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
                terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            elif drive == 'backward':
                tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
                terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Red':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Orange':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Yellow':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Green':
            tn.write("ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN);ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Off':
            tn.write("ev3.Leds.all_off()\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
        elif post_data == 'Left':
            tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            drive = "left"
        elif post_data == 'Forward':
            tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp="+speed+")\n").encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            drive = "forward"
        elif post_data == 'Right':
            tn.write(("motor_left.run_direct(duty_cycle_sp="+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            drive = "right"
        elif post_data == 'Backward':
            tn.write(("motor_left.run_direct(duty_cycle_sp=-"+speed+");motor_right.run_direct(duty_cycle_sp=-"+speed+")\n").encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            drive = "backward"
        elif post_data == 'Stop':
            tn.write("motor_left.run_direct(duty_cycle_sp=0);motor_right.run_direct(duty_cycle_sp=0)\n".encode('utf-8'))
            terminal = terminal+tn.read_until(">>> ".encode('utf-8')).decode('utf-8')
            drive = "stop"
        self._redirect('/')  # Redirect back to the root url
        
        return tn
        return post_data_ip
        return connected
        return speed
        return drive
        return terminal
        return page

# Create Webserver
if __name__ == '__main__':
    http_server = HTTPServer((ip_address, host_port), MyServer)
#    http_server.socket = ssl.wrap_socket (http_server.socket, # Secure Sockets Layer
#        keyfile="ssl/key.pem", 
#        certfile='ssl/cert.pem', server_side=True)
    print("Server Starts - %s:%s" % (ip_address, host_port))
    webbrowser.open_new('http://%s:%s' %  (ip_address, host_port)) # Open in browser automatically

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
        print("\n-------------------EXIT-------------------")
