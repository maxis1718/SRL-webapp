#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cgi
import cgitb; cgitb.enable()

print "Content-type: text/html\n\n"

PORT = 9901

if __name__ == '__main__':
	import socket
	import sys

	if len(sys.argv) == 2:
		PORT = int(sys.argv[2].strip())
	else:
		PORT = 9901

	print '<!DOCTYPE><html>'
	print '<head>'
	print '''<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="cache-control" content="no-cache"><meta http-equiv="pragma" content="no-cache"><meta http-equiv="expires" content="0">'''
	print '''<meta http-equiv="X-UA-Compatible" content="IE=edge" /><link type="text/css" rel="stylesheet" href="index.css" /><title>Sinica SRL</title>'''
	print '</head>'

	print '''<h3><b> Sinica Semantic Role Labeling (SRL) System </b></h3>'''
	
	print '''<form method="post" action="srl-web.py">'''
	print '''<div><textarea name="tree" rows="5" cols="120" class="maxis-textarea"></textarea></div>'''
	print '''<div id="hint"># input example: <span>VP(Head:VC:找出|NP(VP‧的(head:VP(D:可能|Head:VJ:包含)|Head:DE:的)|Head:Na:詞))</span></div>'''
	print '''<p><input type="submit" value="label" class="maxis-button"></p>'''
	print '</form>'


	form = cgi.FieldStorage()
	HOST = "localhost"
	data = form.getvalue('tree')

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.sendall(data + "\n")
	
	received = sock.recv(1024)
	sock.close()
	
	print """<p><b>Unannotated:</b></p>"""
	print '''<div class='annot' id='unannotated'>'''
	print data
	print '''</div>'''

	print """<p><b>Annotated:</b></p>"""
	print '''<div class='annot' id='annotated'>'''
	print received
	print '''</div>'''
	print """ </body> </html>"""
	
