#!/usr/bin/python
from gpiozero       import Motor
from time           import sleep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse       import parse_qs
import threading

# robot motor pins
motorL = Motor(2,  3)
motorR = Motor(4, 17)

# webserver configuration
hostName = ''
serverPort = 8080

# populate page content
page = ""
with open( 'page.html', 'r' ) as file:
	page = file.read()

# global variables
direction = ''
notStopped = True

class MyServer( BaseHTTPRequestHandler ):
	def do_GET( self ):
		self.send_response( 200 )
		self.send_header( "Content-type", "text/html; charset=utf-8" )
		self.end_headers()
		self.wfile.write( page )
	def do_POST( self ):
		global direction
		self.send_response( 200 )
		self.send_header( "Content-type", "text/html; charset=utf-8" )
		content_length = int( self.headers['Content-Length'] )
		post_data = self.rfile.read( content_length )
		data = parse_qs( post_data )
		self.end_headers()
		self.wfile.write( page )
		try:
			direction = data[ "direction" ][0]
		except NameError:
			print wtf

def start_webserver():
	webServer = HTTPServer( (hostName, serverPort), MyServer )
	print( "server started http://%s:%s" % (hostName, serverPort) )
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	notStopped = false
	print( "server stopped" )

webserver_thread = threading.Thread( target=start_webserver )
webserver_thread.start()

if __name__ == '__main__':
	while notStopped:
		if direction:
			print "go " + direction
			if direction == 'up':
				motorL.forward()
				motorR.forward()
			elif direction == 'down':
				motorL.backward()
				motorR.backward()
			elif direction == 'left':
				motorL.backward();
				motorR.forward();
			elif direction == 'right':
				motorL.forward();
				motorR.backward();

			isUpDown = direction == 'up' or direction == 'down'

			direction = ''
			if isUpDown:
				sleep( 1 )
			else:
				sleep( 0.5 )
		else:
			motorL.stop()
			motorR.stop()
			sleep( 0.05 )
