#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()

print "Content-type: text/html\n\n"

if __name__ == '__main__':
	import socket
	import sys
	

	print '''<html><head><title>Sinica SRL</title></head>'''
	print '''<body><center><b><h3> Sinica Semantic Role Labeling (SRL) System </h3></b></center>'''
	print '''<form method="post" action="srl-web.py"><div><textarea name="tree" rows="2" cols="120"></textarea></div><div><input type="submit" value="label"></div></form>'''
	
	form = cgi.FieldStorage()
	HOST, PORT = "localhost", 9999
	data = form.getvalue('tree')

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.sendall(data + "\n")

	received = sock.recv(1024)
	sock.close()
	
	print """<html><b>Unannotated:</b><br></html>"""
	print data
	print """<html><b><br><br><br>Annotated:<br></b></html>"""
	print received
	print """ </body> </html>"""


