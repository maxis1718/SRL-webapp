#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()

print "Content-type: text/html\n\n"

if __name__ == '__main__':
	import socket
	import sys

	print '<!DOCTYPE><html>'

	print '''
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<!-- cache : off -->
		<meta http-equiv="cache-control" content="no-cache">
		<meta http-equiv="pragma" content="no-cache">
		<meta http-equiv="expires" content="0">

		<!-- Lastest IE version -->
		<meta http-equiv="X-UA-Compatible" content="IE=edge" />

		<link type="text/css" rel="stylesheet" href="index.css" />

		<title>Sinica SRL</title>

	</head>	
	'''

	print '''<h3><b> Sinica Semantic Role Labeling (SRL) System </b></h3>'''

	print '''	

	<form method="post" action="srl-web.py">
	    <div>
	        <textarea name="tree" rows="5" cols="120" class="maxis-textarea"></textarea>
	    </div>
	    <div id="hint">
	    	# input example: <span>VP(Head:VC:找出|NP(VP‧的(head:VP(D:可能|Head:VJ:包含)|Head:DE:的)|Head:Na:詞))</span>
	    </div>
	    <p>
	        <input type="submit" value="label" class="maxis-button">
	    </p>
	</form>

	'''
	# print '''<html><head><title>Sinica SRL</title></head>'''
	# print '''<body><center><b><h3> Sinica Semantic Role Labeling (SRL) System </h3></b></center>'''
	# print '''<form method="post" action="srl-web.py"><div><textarea name="tree" rows="2" cols="120"></textarea></div><div><input type="submit" value="label"></div></form>'''

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

	print """<p><b>Unannotated:</b><br></p>"""
	print data
	print """<p><b><br><br><br>Annotated:<br></b></p>"""
	print received
	print """ </body> </html>"""