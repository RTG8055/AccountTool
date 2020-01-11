import sqlite3

databaseName = 'example4.db'

conn = sqlite3.connect(databaseName)

c = conn.cursor()


def getNewID(id_name):
    # conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    data = cursor.execute("select last_val from current_id where id_name='{}'".format(id_name))
    data = cursor.fetchone()[0]
    print data
    if(id_name!='user_id'):
        new_id = data[:2] + "{:04d}".format(int(data[2:])+1)
    else:
        new_id = data[:1] + "{:04d}".format(int(data[1:])+1)
    print new_id

    cursor.execute("UPDATE current_id set last_val='{}' where id_name='{}'".format(new_id, id_name))
    conn.commit()
    return new_id

# Create table
c.execute('''CREATE TABLE items
             (ITEM_ID text PRIMARY KEY, Name text, Code text, Description text, curr_qty real)''')

c.execute('''CREATE TABLE daily_inventory
             (ITEM_ID text, Qty real, date text, PRIMARY KEY ('ITEM_id'), FOREIGN KEY(item_id) REFERENCES items(item_id))''')

c.execute('''CREATE TABLE app_users
			 (user_id text, Name text, email text, password text, access_group text, PRIMARY KEY ('user_id'))''')

c.execute('''CREATE TABLE debtors
			 (debtor_id text PRIMARY KEY, name text, address text, balance real)''')

c.execute('''CREATE TABLE creditors
			 (creditor_id text PRIMARY KEY, name text, address text, balance real)''')

c.execute('''CREATE TABLE received
			 (receipt_id text PRIMARY KEY, ITEM_ID text, Qty real, receipt_date text, creditor_id text, vehicle_no text, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(creditor_id) REFERENCES creditors(creditor_id))''')

c.execute('''CREATE TABLE dispatch
 			 (dispatch_id text PRIMARY KEY, ITEM_ID text, Qty real, dispatch_date text, debtor_id text, vehicle_no text, FOREIGN KEY(item_id) REFERENCES items(item_id), FOREIGN KEY(debtor_id) REFERENCES debtors(debtor_id))''')

c.execute('''CREATE TABLE INVOICE
			 (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')

c.execute('''CREATE TABLE INVOICE_DETAILS
			  (bill_no text, item_id, qty real, rate real, amount real, foreign key(bill_no) REFERENCES invoice(bill_no))''')

c.execute('''CREATE TABLE receipts
			 (receipt_no text, receipt_date text, party_id text, amount real)''')


c.execute('''CREATE Table current_id
			 (id_name text, last_val text)''')


c.execute("INSERT INTO current_id VALUES ('item_id','IT0001')")
c.execute("INSERT INTO current_id VALUES ('creditor_id','CR0001')")
c.execute("INSERT INTO current_id VALUES ('debtor_id','DB0001')")
c.execute("INSERT INTO current_id VALUES ('receipt_id','PU0001')")
c.execute("INSERT INTO current_id VALUES ('dispatch_id','SA0001')")
c.execute("INSERT INTO current_id VALUES ('user_id','U0001')")


 # Insert a row of data
c.execute("INSERT INTO app_users VALUES ('U0001','Vijay','abc@gmail.com', '123', 'all_access')")
c.execute("INSERT INTO app_users VALUES ('U0002','Rahul','abcd@gmail.com', '123', 'all_access')")



c.execute("INSERT INTO items(item_id, name, code, description) VALUES ('IT0001', 'pp', '050', 'desc')")
# c.execute("INSERT INTO items(item_id,name, code, description) VALUES ('IT0002', 'marlex', '70', 'desc')")
# c.execute("INSERT INTO items(item_id,name, code, description) VALUES ('IT0003', 'pp', 'rafia', 'rafia')")

conn.commit()

data = c.execute("select * from debtors")
print data
print c.fetchall()

items = ['MRPL OG', 'MRPL FILM', 'MRPL 12T', 'MRPL HR003', 'MRPL 35YR', 'MRPL 12CT', 'OPAL MH13', 'OPAL FILM', 'OPAL R03', 'MITAL M12RR', 'MITAL R03RR', 'MITAL FILM', 'MITAL TF', 'MITAL OG', 'EX METLOCIN', 'EXON 3155', 'TOTAL PP', 'RIL 050', 'RIL 110', 'RIL 350FG', 'RIL 100EY', 'RIL CP080', 'RIL 100NC', 'RIL 1070LA', 'RIL F190', 'HALDIA 5400', 'HALDIA 110', 'HALDIA T103', 'HALDIA FILM']

for i in items:
	item_id = getNewID('item_id')
	print repr("INSERT INTO items(item_id, name, curr_qty) VALUES ('{}', '{}',  0)".format(item_id, i))
	print repr(i.split(' ')[0])
	# c.execute('INSERT INTO items(item_id, name, code, description) VALUES ("'+ item_id + '", "' + i + '", ')
	c.execute("INSERT INTO items(item_id, name, curr_qty) VALUES ('{}', '{}', 0)".format(item_id, i))


c.execute("INSERT INTO debtors(debtor_id, name, address, balance) VALUES ('DB0001', 'rahul', 'hyd',0)")
c.execute("INSERT INTO debtors(debtor_id, name, address, balance) VALUES ('DB0002', 'rishita', 'bom', 0)")

c.execute("INSERT INTO creditors(creditor_id, name, address, balance) VALUES ('CR0001', 'yash', 'bom', 0)")
c.execute("INSERT INTO creditors(creditor_id, name, address, balance) VALUES ('CR0002', 'hardesh', 'del', 0)")

c.execute("INSERT INTO received(receipt_id, item_id, qty,receipt_date, creditor_id) values ('PU0001', 'IT0002', 41200, '2019-12-21', 'CR0001')")
c.execute("INSERT INTO received(receipt_id, item_id, qty,receipt_date, creditor_id) values ('PU0002', 'IT0001', 94120, '2019-12-21', 'CR0002')")


c.execute("INSERT INTO dispatch(dispatch_id, item_id, qty,dispatch_date, debtor_id) values ('SA0001', 'IT0001', 124, '2019-12-10', 'DB0001')")
c.execute("INSERT INTO dispatch(dispatch_id, item_id, qty,dispatch_date, debtor_id) values ('SA0002', 'IT0002', 1245, '2019-12-11', 'DB0002')")
c.execute("INSERT INTO dispatch(dispatch_id, item_id, qty,dispatch_date, debtor_id) values ('SA0003', 'IT0003', 1224, '2019-11-12', 'DB0001')")
c.execute("INSERT INTO dispatch(dispatch_id, item_id, qty,dispatch_date, debtor_id) values ('SA0004', 'IT0001', 6124, '2019-12-9', 'DB0002')")
c.execute("INSERT INTO dispatch(dispatch_id, item_id, qty,dispatch_date, debtor_id) values ('SA0005', 'IT0002', 4124, '2019-12-21', 'DB0001')")


c.execute("UPDATE current_id set last_val='IT0003' where id_name='item_id'")
c.execute("UPDATE current_id set last_val='CR0002' where id_name='creditor_id'")
c.execute("UPDATE current_id set last_val='DB0002' where id_name='debtor_id'")
c.execute("UPDATE current_id set last_val='PU0001' where id_name='receipt_id'")
c.execute("UPDATE current_id set last_val='SA0005' where id_name='dispatch_id'")
c.execute("UPDATE current_id set last_val='U0002' where id_name='user_id'")

 # Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

data = c.execute("select * from received")
print data
print c.fetchall()
conn.close()


