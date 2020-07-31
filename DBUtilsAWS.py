import sqlite3
import pymysql as MySql

# databaseName = 'test2'
# dbname = 'development1'
dbname = 'test2'
host = '18.219.157.18'
user = 'rahul'
password = 'rahul123'
port = 3073

itemsTable = 'items'
debtorsTable = 'debtors'
creditorsTable = 'creditors'
usersTable = 'app_users'


def call_procedure(procedure_name, args):
    conn = MySql.connect(host=host, user=user, password=password, db=dbname)
    c = conn.cursor()
    result = c.callproc(procedure_name, args)
    conn.commit()
    conn.close()
    return result


def updateData(table, columns, values, condition):
    conn = MySql.connect(host=host, user=user, password=password, db=dbname)
    cursor = conn.cursor()
    updateString = ''
    for (c, v) in zip(columns, values):
        updateString += "{}='{}' ".format(c, v)
    updateString += condition
    print("update SQL Statement: ", repr("UPDATE {} set {}".format(table, updateString)))
    cursor.execute("UPDATE {} set {}".format(table, updateString))
    conn.commit()
    conn.close()


def insertInvoiceDetails(bill_no, _item_all, _quantity_all, _rate_all, _amount_all, _type, _bill_date):
    for (item, qty, rate, amt) in zip(_item_all, _quantity_all, _rate_all, _amount_all):
        values = [bill_no, item, qty, rate, amt]
        call_procedure('insert_invoice_details', values)


# def insertData(table, columns, values):
#     conn = MySql.connect(databaseName)
#     # conn = mysql.connect()
#     cursor = conn.cursor()
#     print("Insert SQL Statement: insert into {} ({}) values ({})".format(table, columns, values))
#     data = cursor.execute("insert into {}({}) values ({})".format(table, columns, values))
#     conn.commit()
#     conn.close()
#     return data


def getData(table, columns='*', condition='blank', extra='no'):
    conn = MySql.connect(host=host, user=user, password=password, db=dbname)
    # conn = mysql.connect()
    if (condition != 'blank'):
        finalCondition = "where {}".format(condition)
    else:
        finalCondition = ''

    if (extra != 'no'):
        finalCondition += " {}".format(extra)
    cursor = conn.cursor()
    print("Get Data SQL statement: ", repr("select {} from {} {}".format(columns, table, finalCondition)))
    data = cursor.execute("select {} from {} {}".format(columns, table, finalCondition))
    data = cursor.fetchall()
    conn.close()
    return data

# def updateBalance(party_type,_id,amount,bill_type):
#     table=''
#     condition=''
#     if(party_type == 'debtor'):
#         currBal = getData(debtorsTable, 'balance', "debtor_id = '{}'".format(_id))[0][0]
#         table=debtorsTable
#         condition = "where debtor_id='{}'".format(_id)
#     else:
#         currBal = getData(creditorsTable, 'balance', "creditor_id = '{}'".format(_id))[0][0]
#         table=creditorsTable
#         condition = "where creditor_id='{}'".format(_id)
#     print("current Balance:", repr(currBal))
#     newBal=currBal
#     if(bill_type == 'add'):
#         newBal=currBal + float(amount)
#     else:
#         newBal=currBal - float(amount)
#     print("New Balance:", newBal)
#     updateData(table,['balance'],[newBal],condition)

# def updateQty(item_id, _qty, _type):
#     currQty = getData(itemsTable, 'curr_qty', "item_id = '{}'".format(item_id))[0][0]
#     newQty = currQty
#     if(_type == 'add'):
#         newQty=currQty + float(_qty)
#     else:
#         newQty=currQty - float(_qty)
#     print("new Quantity:", newQty)
#     condition = "where item_id ='{}'".format(item_id)
#     updateData(itemsTable,['curr_qty'],[newQty],condition)
