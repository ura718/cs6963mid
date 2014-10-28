#!/usr/bin/python

import urllib2


for f_lines in open('sites','r').readlines():
    print f_lines
    try:
      response = urllib2.urlopen(f_lines, timeout=10)
      print response.info()
      response.close()
    except urllib2.URLError, e:
      print "There was an error in reading url header: %s" % e




