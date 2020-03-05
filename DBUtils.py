import sqlite3



databaseName = 'example6.db'
itemsTable = 'items'
debtorsTable = 'debtors'
creditorsTable = 'creditors'
usersTable = 'app_users'


def getNewID(id_name):
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()

    data = cursor.execute("select last_val from current_id where id_name='{}'".format(id_name))
    data = cursor.fetchone()[0]
    if(id_name!='user_id'):
        new_id = data[:2] + "{:04d}".format(int(data[2:])+1)
    else:
        new_id = data[:1] + "{:04d}".format(int(data[1:])+1)
    print("new ID created: ", new_id)

    cursor.execute("UPDATE current_id set last_val='{}' where id_name='{}'".format(new_id, id_name))
    conn.commit()
    conn.close()
    return new_id


def insertInvoiceDetails(bill_no,_item_all,_quantity_all,_rate_all,_amount_all,_type,_bill_date):
    for (item,qty,rate,amt) in zip(_item_all,_quantity_all,_rate_all,_amount_all):
        columns = 'bill_no, item_id, qty, rate, amount'
        values = "'{}', '{}', '{}', '{}', '{}'".format(bill_no, item, qty, rate, amt)
        insertData('invoice_details', columns, values)
        if(_type == "sales"):
            updateQty(item,qty,"sub")
            insertData('daily_inventory','item_id, qty, date',"'{}','{}','{}'".format(item,-float(qty),_bill_date))
        else:
            updateQty(item,qty,"add")
            insertData('daily_inventory','item_id, qty, date',"'{}','{}','{}'".format(item,qty,_bill_date))


def updateData(table,columns, values,condition):
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()
    updateString=''
    for (c,v) in zip(columns, values):
        updateString += "{}='{}' ".format(c,v)
    updateString+= condition
    print("update SQL Statement: ", repr("UPDATE {} set {}".format(table,updateString)))
    cursor.execute("UPDATE {} set {}".format(table,updateString))
    conn.commit()
    conn.close()

def insertData(table, columns, values):
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    print("Insert SQL Statement: insert into {} ({}) values ({})".format(table, columns, values))
    data = cursor.execute("insert into {}({}) values ({})".format(table, columns, values))
    conn.commit()
    conn.close()
    return data


def getData(table, columns='*',condition='blank'):
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    if(condition != 'blank'):
        finalCondition = "where {}".format(condition)
    else:
        finalCondition = ''
    cursor = conn.cursor()
    print("Get Data SQL statement: ", repr("select {} from {} {}".format(columns, table, finalCondition)))
    data = cursor.execute("select {} from {} {}".format(columns, table, finalCondition))
    data = cursor.fetchall()
    conn.close()
    return data

def updateBalance(party_type,_id,amount,bill_type):
    table=''
    condition=''
    if(party_type == 'debtor'):
        currBal = getData(debtorsTable, 'balance', "debtor_id = '{}'".format(_id))[0][0]
        table=debtorsTable
        condition = "where debtor_id='{}'".format(_id)
    else:
        currBal = getData(creditorsTable, 'balance', "creditor_id = '{}'".format(_id))[0][0]
        table=creditorsTable
        condition = "where creditor_id='{}'".format(_id)
    print("current Balance:", repr(currBal))
    newBal=currBal
    if(bill_type == 'add'):
        newBal=currBal + float(amount)
    else:
        newBal=currBal - float(amount)
    print("New Balance:", newBal)
    updateData(table,['balance'],[newBal],condition)

def updateQty(item_id, _qty, _type):
    currQty = getData(itemsTable, 'curr_qty', "item_id = '{}'".format(item_id))[0][0]
    newQty = currQty
    if(_type == 'add'):
        newQty=currQty + float(_qty)
    else:
        newQty=currQty - float(_qty)
    print("new Quantity:", newQty)
    condition = "where item_id ='{}'".format(item_id)
    updateData(itemsTable,['curr_qty'],[newQty],condition)