import sqlite3

conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE items
             (ITEM_ID INTEGER PRIMARY KEY, Name text, Code text, Description text, dealer text)''')

c.execute('''CREATE TABLE inventory
             (ITEM_ID INTEGER, Qty real, PRIMARY KEY ('ITEM_id'), FOREIGN KEY(item_id) REFERENCES items(item_id))''')

c.execute('''CREATE TABLE app_users
			 (user_id text, Name text, email text, password text, access_group text, PRIMARY KEY ('user_id'))''')

c.execute('''CREATE TABLE debtors
			 (debtor_id INTEGER PRIMARY KEY, name text, location text)''')

c.execute('''CREATE TABLE creditors
			 (creditor_id INTEGER PRIMARY KEY, name text, location text)''')

c.execute('''CREATE TABLE received
			 (receipt_no INTEGER PRIMARY KEY, ITEM_ID text, Qty real, receipt_date text, creditor_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(creditor_id) REFERENCES creditors(creditor_id))''')

c.execute('''CREATE TABLE dispatch
 			 (dispatch_no INTEGER PRIMARY KEY, ITEM_ID text, Qty real, dispatch_date text, debtor_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(debtor_id) REFERENCES debtors(debtor_id))''')


 # Insert a row of data
c.execute("INSERT INTO app_users VALUES ('u01','Vijay','abc@gmail.com', '123', 'all_access')")
c.execute("INSERT INTO app_users VALUES ('u02','Rahul','abcd@gmail.com', '123', 'all_access')")



c.execute("INSERT INTO items(name, code, description, dealer) VALUES ('pp', '050', 'desc', 'reliance')")
c.execute("INSERT INTO items(name, code, description, dealer) VALUES ('marlex', '70', 'desc', 'MRPL')")
c.execute("INSERT INTO items(name, code, description, dealer) VALUES ('pp', 'rafia', 'rafia', 'reliance')")
c.execute("INSERT INTO debtors(name, location) VALUES ('rahul', 'hyd')")
c.execute("INSERT INTO debtors(name, location) VALUES ('rishita', 'bom')")
c.execute("INSERT INTO creditors(name, location) VALUES ('yash', 'bom')")
c.execute("INSERT INTO creditors(name, location) VALUES ('hardesh', 'del')")

c.execute("INSERT INTO dispatch(item_id, qty,receipt_date, creditor_id) values (2, 124, '2019-12-10', 2)")
c.execute("INSERT INTO dispatch(item_id, qty,receipt_date, creditor_id) values (1, 124245, '2019-12-11', 1)")
c.execute("INSERT INTO dispatch(item_id, qty,receipt_date, creditor_id) values (2, 1224, '2019-11-12', 2)")
c.execute("INSERT INTO dispatch(item_id, qty,receipt_date, creditor_id) values (1, 6124, '2019-12-9', 1)")
c.execute("INSERT INTO dispatch(item_id, qty,receipt_date, creditor_id) values (2, 4124, '2019-12-21', 2)")

 # Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

data = c.execute("select * from received")
print data
print c.fetchall()
conn.close()