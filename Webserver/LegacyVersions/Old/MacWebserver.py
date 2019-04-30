# Dummy Site, Doesn't actually control to EV3
# Used to test http.serve package
# run with python3

from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '10.0.0.173'  # Change this to your Raspberry Pi IP address
host_port = 8000


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        html = '''
           <html>
           <body style="width:960px; margin: 20px auto;">
           <h1>Control EV3 through a telnet connection Demo</h1>
           <p>Use the buttons to control the LEDs on the EV3</p>
           <form action="/" method="POST">
               LED :
               <input type="submit" name="submit" value="Red">
               <input type="submit" name="submit" value="Orange">
               <input type="submit" name="submit" value="Yellow">
               <input type="submit" name="submit" value="Green">
               <input type="submit" name="submit" value="Off">
           </form>
           </body>
           </html>
        '''
        temp = "1"
        self.do_HEAD()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        """ do_POST() can be tested using curl command
            'curl -d "submit=On" http://server-ip-address:port'
        """
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = post_data.split("=")[1]  # Only keep the value

        # LED setup goes here

        if post_data == 'Red':
            i = 1# Insert Code 
        elif post_data == 'Orange':
            i = 1# Insert Code 
        elif post_data == 'Yellow':
            i = 1# Insert Code 
        elif post_data == 'Green':
            i = 1 # Insert Code 
        else:
            i = 1# Insert Code 
        print("LED is {}".format(post_data))
        self._redirect('/')  # Redirect back to the root url


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
