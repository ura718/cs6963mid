#!/usr/bin/python

import urllib2

HOST = ['http://www.google.com', 'http://facebook.com']


for f_line in HOST:
	response = urllib2.urlopen(f_line)
	print response.info()
	print "\n"

	response.close()
