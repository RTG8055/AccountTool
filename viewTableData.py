import sqlite3

conn = sqlite3.connect('example2.db')

c = conn.cursor()

# data = c.execute("select * from received")
data = c.execute("select * from dispatch")
print data
print c.fetchall()
conn.close()