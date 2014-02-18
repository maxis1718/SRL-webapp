#!C:\Python27\python.exe -u
#!/usr/bin/env python 
import cgi
import cgitb; cgitb.enable()  # for troubleshooting

if __name__ == "__main__":
 import sys
 try:
	print """
	<html>
 
	<head><title>Sinica SRL</title></head>

	<body>
	<center><b>
	<h3> Sinica Semantic Role Labeling (SRL) System </h3></b>
	</center>

	<form method="post" action="srl-web.py">
	<div><textarea name="tree" rows="2" cols="120"></textarea></div>
	<div><input type="submit" value="label"></div>
	</form>
	"""
	
	
 except:
	print >>sys.stderr, __doc__
	raise
