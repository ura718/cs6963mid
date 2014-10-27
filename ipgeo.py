#!/usr/bin/python

#
# This code was tested on RedHat6.5
# Requirements
# 	jwhois 		= rpm linux
#	subprocess	= python module 
#


import socket
import subprocess
import re
import time

 

 
# Loop over each line in a open file
for f_lines in open('sites','r').readlines():
  f_lines = f_lines.replace("http://","")	# remove http:// from url 
  f_lines = f_lines.replace("https://","")	# remove https:// from url 
  f_lines = f_lines.replace("www.","")		# remove www. from url
  f_lines = (f_lines).split('/')[0]			# remove everything after domain
  print f_lines 
  
  HOST = f_lines.rstrip()					# strip '\n' from each line
  print "QUERY: %s" % HOST
  p = subprocess.Popen(['whois %s' % (str(HOST))], shell=True, stdout=subprocess.PIPE)
  output, err = p.communicate()
  output = output.split('\n')				# split each line of string output by '\n'



  # Extract certain information from whois output
  info = []
  for o_lines in (output):
	if re.search(r"^Domain", o_lines):		# search(pattern,string)
	  info.append(o_lines)
	if re.search(r"^Updated", o_lines):
	  info.append(o_lines)
	if re.search(r"^Created", o_lines):
	  info.append(o_lines)
	if re.search(r"^Admin", o_lines):
	  info.append(o_lines)
	if re.search(r"^Registrar", o_lines):
	  info.append(o_lines)
	if re.search(r"^Registrant", o_lines):
	  info.append(o_lines)
	if re.search(r"^Tech", o_lines):
	  info.append(o_lines)
	if re.search(r"^Name", o_lines):
	  info.append(o_lines)



  # See what info has been collected from whois output
  for i_lines in (info):
  	print i_lines

  print "\n------SLEEPING 5 sec-------------\n"
  time.sleep(5)			# sleep required otherwise new query cant be spawned
