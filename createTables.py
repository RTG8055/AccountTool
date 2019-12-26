import sqlite3

conn = sqlite3.connect('example3.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE items
             (ITEMID INTEGER PRIMARY KEY, Name text, Code text, Description text, dealer text)''')

c.execute('''CREATE TABLE inventory
             (ITEM_ID INTEGER, Qty real, PRIMARY KEY ('ITEM_id'), FOREIGN KEY(item_id) REFERENCES items(item_id))''')

c.execute('''CREATE TABLE app_users
			 (user_id text, Name text, email text, password text, access_group text, PRIMARY KEY ('user_id'))''')

c.execute('''CREATE TABLE debtors
			 (debtor_id INTEGER PRIMARY KEY, name text, location text)''')

c.execute('''CREATE TABLE creditors
			 (creditor_id INTEGER PRIMARY KEY, name text, location text)''')

c.execute('''CREATE TABLE recieved
			 (receipt_no INTEGER PRIMARY KEY, ITEM_ID text, Qty real, receipt_date date, creditor_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(creditor_id) REFERENCES creditors(creditor_id))''')

c.execute('''CREATE TABLE dispatch
 			 (dispatch_no INTEGER PRIMARY KEY, ITEM_ID text, Qty real, dispatch_date date, debtor_id INTEGER, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(debtor_id) REFERENCES debtors(debtor_id))''')


# Insert a row of data
c.execute("INSERT INTO app_users VALUES ('u01','Vijay','abc@gmail.com', '123', 'all_access')")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()