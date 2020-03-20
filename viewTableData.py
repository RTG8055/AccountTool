import sqlite3

conn = sqlite3.connect('example6.db')

c = conn.cursor()

data = c.execute("select * from creditors where balance = 'nan'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0022'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0023'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0024'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0026'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0027'")
# c.execute("UPDATE creditors set balance='0.0' where creditor_id='CR0037'")
# conn.commit()
print c.fetchall()

# data = c.execute("select * from invoice")
# print "----------invoice---------------"
# print data
# print c.fetchall()

# data = c.execute("select * from items")
# print "----------items---------------"
# print data
# print c.fetchall()


# data = c.execute("select * from invoice_details")
# print "----------invoice details---------------"
# print data
# print c.fetchall()


# data = c.execute("select * from debtors")
# print "----------debtors---------------"
# print data
# print c.fetchall()

# data = c.execute("select item_id, qty, rate, amount from INVOICE_DETAILS where bill_no='B00005'")
# print "----------invoice query---------------"
# print data
# print c.fetchall()



# print "----------creditors---------------"
# data = c.execute("select * from creditors")
# print data
# print c.fetchall()




# c.execute("UPDATE current_id set last_val='IT0030' where id_name='item_id'")
# conn.commit()
conn.close()

# <sqlite3.Cursor object at 0x7fae73199ea0>
# [(u'B00002', u'None', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00003', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00004', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00005', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00006', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00007', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00008', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06'), (u'B00009', u'DB0001', u'', 1200.0, u'sales', u'2020-01-06')]
# <sqlite3.Cursor object at 0x7fae73199ea0>
# [(u'B00005', u'IT0006', 12.0, 100.0, 1200.0), (u'B00006', u'IT0006', 12.0, 100.0, 1200.0), (u'B00007', u'IT0006', 12.0, 100.0, 1200.0), (u'B00008', u'IT0006', 12.0, 100.0, 1200.0), (u'B00009', u'IT0006', 12.0, 100.0, 1200.0)]
# [Finished in 0.0s]