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


 
def WHOIS():
 
  # Loop over each line in a open file
  for f_lines in open('sites','r').readlines():

    # ISOLATE DOMAIN FROM URL EXTRAS 
    f_lines = f_lines.replace("http://","")	# remove http:// from url 
    f_lines = f_lines.replace("https://","")	# remove https:// from url 
    f_lines = f_lines.replace("www.","")		# remove www. from url
    f_lines = (f_lines).split('/')[0]			# remove everything after domain
    f_lines = f_lines.strip('\n')				# remove newline
    #print f_lines



    # GET IP FROM HOSTNAME 
    IP = socket.gethostbyname(f_lines)		# get hostname ip address
    #print IP



    # RUN SHELL COMMAND TO QUERY WHOIS DB 
    HOST = f_lines
    print "QUERY: %s : %s" % (HOST,IP)
    p = subprocess.Popen(['whois %s' % (str(HOST))], shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    output = output.split('\n')				# split each line of string output by '\n'



    # EXTRACT SPECIFIC INFORMATION FROM WHOIS OUTPUT 
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



    # SHOW END RESULT FROM WHOIS OUTPUT
    for i_lines in (info):
  	  print i_lines


    print "\n------SLEEPING 5 sec-------------\n"
    time.sleep(5)			# sleep required otherwise new query cant be spawned




def main():
  WHOIS() 



if __name__ == '__main__':
	main()

