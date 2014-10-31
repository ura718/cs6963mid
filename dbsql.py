#!/usr/bin/python

#
# sqlite3 <file.db>
# .tables 						= list tables
# .schema <table> 				= get sql schema when creating a table
# pragma table_info('<table>')	= list columns 
#

import sqlite3


# Create database
def sqlDB():
  DBFILE = 'data.db'
  try:
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS mydata")			# Drop table 'mydata'
    #cursor.execute("CREATE TABLE mydata(DATA char(200))")   # create table 'mydata' with column 'DATA'
    cursor.execute("CREATE TABLE mydata(DATA text)")   # create table 'mydata' with column 'DATA'
    conn.commit()
    conn.close()
  except sqlite3.OperationalError, e:
    print "Database already exists"
    pass



def addtoDB(i_data):
  DBFILE = 'data.db'

  # INSERT i_data INTO DB
  try:
    conn = sqlite3.connect(DBFILE)
    conn.execute("INSERT INTO mydata (DATA) VALUES(?)", (i_data,)) # NOTE: Need comma ',' after i_data
    conn.commit()
    conn.close()
  except:
    raise




  # SELECT DATA FROM DB
  try:
    conn = sqlite3.connect(DBFILE)
    cursor = conn.execute("SELECT * from mydata")
    for row in cursor:
      print row
    conn.close()
  except:
    raise
  



sqlDB()

domain=['facebook.com : 127.0.0.1', 'google.com']
for i_data in domain:
  print i_data
  addtoDB(i_data) 
  
