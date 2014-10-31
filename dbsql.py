#!/usr/bin/python


import sqlite3


# Create database
def sqlDB():
  DBFILE = 'data.db'
  try:
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS mydata")
    cursor.execute("CREATE TABLE mydata(Name TEXT)") 
    conn.commit()
  except sqlite3.OperationalError, e:
    print "Database already exists"
    pass



# Add to database
def addtoDB(i_data):
  DBFILE = 'data.db'
  print i_data
  try:
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mydata VALUES(?)", (str(i_data)))
    #cursor.execute("INSERT INTO mydata VALUES('hello')")
    print cursor.execute('SELECT * from mydata')
    conn.commit()
  except:
    pass




sqlDB()

domain=['facebook.com', 'google.com']
for i_data in domain:
  addtoDB(i_data) 
  
