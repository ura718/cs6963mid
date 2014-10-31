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





def CHECK_FILES(f_report):

  # Dont use script name to create reports
  if os.path.basename(__file__) == f_report:
    print "Error: Cant use running script as name for reports. Pick different name"    
    exit(1)

  # Dont use sites url file to create reports
  if 'sites' == f_report:
    print "Error: Cant use sites as name for report creation. Pick a different name" 
    exit(1)



  # We need a sites file with all the urls. Does it exist?...
  try: 
    f = open('sites','r')
  except IOError, e:
 	print 'File Not Found: Please provide sites file with urls '
	exit(1)
  else:
    f.close()


  # Does reports exist? If so delete it...
  try:
    fo = open(f_report, 'r')      
    if fo:
      os.remove(f_report)
    fo.close()
  except IOError, e:
    pass





def DOMAIN():
  domain=[]
  # Loop over each line in a open file
  for f_lines in open('sites','r').readlines():

    # ISOLATE DOMAIN FROM URL EXTRAS 
    f_lines = f_lines.replace("http://","")	    # remove http:// from url 
    f_lines = f_lines.replace("https://","")	# remove https:// from url 
    f_lines = f_lines.replace("www.","")		# remove www. from url
    f_lines = (f_lines).split('/')[0]			# remove everything after domain
    f_lines = '.'.join((f_lines).split('.')[-2:]) # remove subdomains and take last 2 elements only
    f_lines = f_lines.strip('\n')				# remove newline
    domain.append(f_lines)

  return (domain)




 
def WHOIS(dnsname):
  i_whois=[] 	# use to store incomplete 'whois' information (e.g: excludes banners)
  a_whois=[]	# use to store all 'whois' information (e.g: includes banners and everything)



  # Loop over each line in dns names
  for f_lines in dnsname:
    # RUN SHELL COMMAND TO QUERY WHOIS DB 
    HOST = f_lines
    print "QUERY: %s " % (HOST)
    p = subprocess.Popen(['whois %s' % (str(HOST))], shell=True, stdout=subprocess.PIPE)
    output, err = p.communicate()
    output = output.split('\n')				# split each line of string output by '\n'



    # APPEND ALL WHOIS INFO INCLUDING BANNERS (e.g: use for reports)
    for a_lines in (output):
      a_whois.append(a_lines)



    # EXTRACT SPECIFIC INFORMATION FROM WHOIS OUTPUT EXCLUDING BANNERS (e.g: use for DB storage)
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

    info.append('\n')

    # SHOW END RESULT FROM WHOIS OUTPUT
    for i_lines in (info):						
      #print i_lines
      i_whois.append(i_lines)


    print "\n------SLEEPING 5 sec-------------\n"
    time.sleep(5)			# sleep required otherwise new query cant be spawned


  return (a_whois, i_whois)			# return information 





def IPDNS(dnsname):
  ipaddr = []								# create empty array
  # Loop over each item in dnsnames
  for f_lines in dnsname:

    # GET IP FROM HOSTNAME 
    IP = socket.gethostbyname(f_lines)		# get hostname ip address
    ipaddr.append(IP)
    #print "%s : %s " % (f_lines,IP)

  return ipaddr





def URLHEADER():
  header = []								# create empty array list
  for f_lines in open('sites','r').readlines():
    f_lines = (f_lines).split('//',1)				# remove everything after domain
    f_lines = f_lines[0] + '//' + f_lines[1].split('/',1)[0]  # extract domainname with http://
    f_lines = f_lines.strip('\n')					# remove newline
    #print f_lines
    try:
      response = urllib2.urlopen(f_lines, timeout=10)
      #print response.info()
      header.append(response.info())
      response.close()
    except urllib2.URLError, e:
      print "There was an error in reading url header: %s" % e

  return (header)





def GEOIP(ipaddr):
  i_geo = []						# setup empty array list
  for ip in ipaddr:
    match = geolite2.lookup(ip)
    #print match.ip					# ip address
    i_geo.append(match.ip)
    #print match.country				# country code as ISO
    i_geo.append(match.country)
    #print match.continent			# continent code as ISO
    i_geo.append(match.continent)
    #print match.timezone			# timezone if available as tzinfo name
    i_geo.append(match.timezone)
    #print match.subdivisions		# list of ISO codes as immutable set
    i_geo.append(match.subdivisions)
    #print match.location			# latitude and longitude tuples
    i_geo.append(match.location)
    #print '\n'
    i_geo.append('\n')

  return i_geo 





def main():
  # Help Menu
  parser = argparse.ArgumentParser()
  parser.add_argument('-r', help='Create Report File')
  parser.add_argument('-d', help='Create SQL DB')
  args=parser.parse_args()


  # OPTION FOR GENERATING REPORTS
  if args.r == None:
    f_report=None
    print '[-] Creating Reports File'
  elif args.r:
    f_report = args.r
    print '[+] Creating Reports File: %s' % f_report
    CHECK_FILES(f_report)				# Check if url site file exists. And remove any old report file


  if args.d == None:
  	print '[-] Creating SQL DB'
  elif args.d:
    print '[+] Creating SQL DB:' 

 

 




  ''' RUN DNSNAME '''

  dnsname=DOMAIN()				# strip urls and only get domain name (e.g: example.com)

  # APPEND dnsnames TO REPORT FILE
  if f_report == None:  
    for i in dnsname:
      print i
  elif f_report:
    try: 
      fo = open(f_report,'a')
      for i in dnsname:
        print i
        fo.write(i)
        fo.write('\n')
    except IOError, e:
 	  print 'Cant append reports file: %s ' % e
	  exit(1)
    else:
      fo.close()

  
  print "\n---------------------------------\n"




  ''' RUN WHOIS '''

  (a_whois, i_whois)=WHOIS(dnsname) # run whois against domain name

  # APPEND a_whois TO REPORT FILE OR PRINT i_whois TO SCREEN
  if f_report == None:
    for i in i_whois:
      print i 
  elif f_report:
    try: 
      fo = open(f_report,'a')
      for i in a_whois:
        print i
        fo.write(i)
        fo.write('\n')
    except IOError, e:
 	  print 'Cant append to reports file: %s ' % e
	  exit(1)
    else:
      fo.close()
  


  print "\n---------------------------------\n"

  ''' RUN IPDNS '''

  # APPEND ipaddr TO REPORT FILE 
  ipaddr=IPDNS(dnsname)			# return ip addresses

  if f_report == None:
    for i in range(0,len(dnsname)):
      print dnsname[i] + ' : ' + ipaddr[i]
  elif f_report:
    try: 
      fo = open(f_report,'a')
      for i in range(0,len(dnsname)):
        print dnsname[i] + ' : ' + ipaddr[i]
        fo.write(dnsname[i] + ' : ' + ipaddr[i])
        fo.write('\n')
    except IOError, e:
 	  print 'Cant append to reports file: %s ' % e
	  exit(1)
    else:
      fo.close()




  print "\n---------------------------------\n"

  # APPEND HEADER TO REPORT FILE 
  header=URLHEADER() 				# get header for each url link 

  if f_report == None:
    for i in header:
      print i
  elif f_report:
    try: 
      fo = open(f_report,'a')
      for i in header:
        print i
        fo.write(str(i))
        fo.write('\n')
    except IOError, e:
 	  print 'Cant append to reports file: %s ' % e
	  exit(1)
    else:
      fo.close()




  print "\n---------------------------------\n"

  # APPEND GEOLOC TO REPORT FILE
  geoloc=GEOIP(ipaddr)				# get geo location against each url link
  
  if f_report == None:
    for i in geoloc:
      print i
  elif f_report:
    try: 
      fo = open(f_report,'a')
      for i in geoloc:
        print i
        fo.write(str(i))
        fo.write('\n')
    except IOError, e:
 	  print 'Cant append to reports file: %s ' % e
	  exit(1)
    else:
      fo.close()

  



if __name__ == '__main__':
	main()

