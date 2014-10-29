#!/usr/bin/python

#
# http://pythonhosted.org/python-geoip/
# install module python-geoip-geolite2
# install module python-geoip

from geoip import geolite2


data = ['173.252.120.6', '173.194.123.3', '209.172.54.83']

for ip in data:
	match = geolite2.lookup(ip)
	print match.ip
	print match.country
	print match.continent
	print match.timezone
	print match.subdivisions
	print match.location
	print '\n'
