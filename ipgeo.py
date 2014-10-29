#!/usr/bin/python

#
# Author: Yuri Medvinsky
# cs6963 - midterm
#
# This code was tested on RedHat6.5
# Requirements
# 	jwhois 		= rpm linux (jwhois-4.0-19.el6.x86_64)
#
#   http://pythonhosted.org/python-geoip/
#   install module python-geoip-geolite2
#   install module python-geoip


import argparse
import urllib2
import subprocess
import socket
import time
import sys
import re
import os
from geoip import geolite2





def CHECK_FILES():

  # We need a sites file with all the urls. Does it exist?...
  try: 
    f = open('sites','r')
  except IOError, e:
 	print 'File Not Found: Please provide sites file with urls '
	exit(1)
  else:
    f.close()


  # Does reports.txt exist? If so delete it...
  try:
    fo = open('report.txt', 'r')      
    if fo:
      os.remove('report.txt')
    fo.close()
  except IOError, e:
    pass





def DOMAIN():
  domain=[]
  # Loop over each line in a open file
  for f_lines in open('sites','r').readlines():

    # ISOLATE DOMAIN FROM URL EXTRAS 
    f_lines = f_lines.replace("http://","")	# remove http:// from url 
    f_lines = f_lines.replace("https://","")	# remove https:// from url 
    f_lines = f_lines.replace("www.","")		# remove www. from url
    f_lines = (f_lines).split('/')[0]			# remove everything after domain
    f_lines = '.'.join((f_lines).split('.')[-2:]) # remove subdomains and take last 2 elements only
    f_lines = f_lines.strip('\n')				# remove newline
    domain.append(f_lines)

  return (domain)




 
def WHOIS(dnsname):
  # Loop over each line in dns names
  for f_lines in dnsname:

    # RUN SHELL COMMAND TO QUERY WHOIS DB 
    HOST = f_lines
    print "QUERY: %s " % (HOST)
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





def IPDNS(dnsname):
  ipaddr = []								# create empty array
  # Loop over each item in dnsnames
  for f_lines in dnsname:

    # GET IP FROM HOSTNAME 
    IP = socket.gethostbyname(f_lines)		# get hostname ip address
    ipaddr.append(IP)
    print "%s : %s " % (f_lines,IP)

  return ipaddr


def URLHEADER():
  for f_lines in open('sites','r').readlines():
    f_lines = f_lines.rstrip()
    print f_lines
    try:
      response = urllib2.urlopen(f_lines, timeout=10)
      print response.info()
      response.close()
    except urllib2.URLError, e:
      print "There was an error in reading url header: %s" % e




def GEOIP(ipaddr):
  for ip in ipaddr:
	match = geolite2.lookup(ip)
	print match.ip					# ip address
	print match.country				# country code as ISO
	print match.continent			# continent code as ISO
	print match.timezone			# timezone if available as tzinfo name
	print match.subdivisions		# list of ISO codes as immutable set
	print match.location			# latitude and longitude tuples
	print '\n'

  




def main():
  # Help Menu
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', help='Create Report File')
  parser.add_argument('-d', help='Create SQL DB')
  args=parser.parse_args()

  if args.r == None:
	print '[-] Creating Reports File'
  elif args.r:
    print '[+] Creating Reports File'
		
  if args.d == None:
  	print '[-] Creating SQL DB'
  elif args.d:
  	print '[+] Creating SQL DB'



  CHECK_FILES()				# Check all necessary files exist before running program
  dnsname = DOMAIN()		# strip urls and only get domain name (e.g: example.com)
  #WHOIS(dnsname) 			# run whois against domain name
  ipaddr=IPDNS(dnsname)		# return ip addresses
  #URLHEADER()				# get header for each url link 
  #GEOIP(ipaddr)				# get geo location against each url link


  




if __name__ == '__main__':
	main()

