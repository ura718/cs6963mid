#!/usr/bin/python

#
# Create url.kml file to be used for google earth
#

import simplekml

kml=simplekml.Kml()
kml.newpoint(name="Facebook.com", coords=[(18.432314,-33.988862)])
kml.newpoint(name="google.com", coords=[(28.432319,-13.788862)])
kml.save("url.kml")
