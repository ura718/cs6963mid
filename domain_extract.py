#!/usr/bin/python

for f_lines in open('sites','r').readlines():

    # ISOLATE DOMAIN FROM URL EXTRAS
    f_lines = f_lines.replace("http://","") # remove http:// from url
    f_lines = f_lines.replace("https://","")    # remove https:// from url
    f_lines = f_lines.replace("www.","")        # remove www. from url
    f_lines = (f_lines).split('/')[0]           # remove everything after domain
    f_lines = '.'.join((f_lines).split('.')[-2:])
    f_lines = f_lines.strip('\n')               # remove newline
    print f_lines
