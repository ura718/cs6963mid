#!/usr/bin/python

import os



# Check if file exists and then remove it
try:
  fo = open('report.txt', 'r')		
  if fo:
    os.remove('report.txt') 
  fo.close()
except IOError, e:
  pass


try:
  fo = open("report.txt", "a")			# open file for append 
  print "#" + "="*70					# print '=' multiple times on one line
  fo.write("#" + "="*70 + "\n")
  fo.close()
except IOError, e:
  print "Cant append to reports.txt file"
