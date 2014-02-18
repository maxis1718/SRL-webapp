#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
fname  = form.getfirst("fname")			# Pull fname field data
lname  = form.getfirst("lname")			# Pull lname field data
secret = form.getfirst("secretsquirrel")	# Pull secretsquirrel 

print "Content-Type: text/html; charset=UTF-8"	# Print headers
print ""					# Signal end of headers

print '''
<html>
<body>
'''
print "First name:",fname
print "<br  />"
print "Last name:",lname
print "<br  />"
print "Whole name:",fname+" "+lname
print "<br  />"
print "The secret was:",secret
print '''
</body>
</html>
'''
