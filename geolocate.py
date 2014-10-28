#!/usr/bin/python

#
# http://pythonhosted.org/python-geoip/
# install module python-geoip-geolite2
# install module python-geoip

from geoip import geolite2


match = geolite2.lookup('173.252.120.6')
print match.country
print match.continent
print match.timezone
print match.subdivisions
print match.location
print match.ip
