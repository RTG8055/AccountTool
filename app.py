import requests
from DBUtils import *
import locale
locale.setlocale(locale.LC_MONETARY, 'en_IN')

import datetime

from flask import Flask, render_template, redirect, json, request, session, Markup, flash, jsonify
import sqlite3

app = Flask(__name__)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 

databaseName = 'example6.db'
itemsTable = 'items'
debtorsTable = 'debtors'
creditorsTable = 'creditors'
usersTable = 'app_users'

@app.route('/')
@app.route('/home')
def main():
    if(session.get('user_id')):
        return showWebPage('home.html', {'namex':session.get('name')})
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dispatch')
def dispatch():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id')
            itemDropDown = createDropDown(itemData, 'item', 'Select Item', 1, 0)

            debtorsData = getData(debtorsTable,'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, 'debtor','Select Party Name', 1, 0)
            
            return showWebPage('dispatch.html', {'items':itemDropDown, 'debtors':debtorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/dispatch', methods=['POST'])
def enterDispatch():
    try:
        _item_id = request.form.get('item')
        _debtor_id = request.form.get('debtor')
        _quantity = request.form.get('quantity')
        _dispatch_date = request.form.get('dispatch_date')

        dispatch_id = getNewID('dispatch_id')
        if(request.form.get('vehicle_no')):
            _vehicle_no=request.form.get('vehicle_no')
            columns='dispatch_id, item_id, qty,dispatch_date, debtor_id, vehicle_no'
            values = "'{}', '{}', '{}', '{}', '{}'".format(dispatch_id, _item_id, _quantity, str(_dispatch_date), _debtor_id, _vehicle_no)
        else:
            columns='dispatch_id, item_id, qty,dispatch_date, debtor_id'
            values = "'{}', '{}', '{}', '{}', '{}'".format(dispatch_id, _item_id, _quantity, str(_dispatch_date), _debtor_id)
        insertData('dispatch',columns, values)
    except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return redirect('/dispatch')


@app.route('/viewparty')
def viewParty():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('viewParties.html',{})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})


@app.route('/additem')
def additem():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('addItem.html',{'display':'none'})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/additem', methods=['POST'])
def addItemDB():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            
            _item_name = request.form.get('item').strip().upper()
            _qty = request.form.get('qty')

            if(not checkPartyItemExists(_item_name, 'item')):
                address = ''
                item_id = getNewID('item_id')
                columns = "item_id, name,curr_qty"
                values = "'{}','{}',{}".format(item_id,_item_name,_qty)
                insertData(itemsTable, columns,values)
                return showWebPage('addItem.html',{'error':'Item Added', 'display':'true'})

            else:
                e= {'error':'Item Already Exists', 'display':'true'}
            
                return showWebPage('addItem.html',e)
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/addparty')
def addParty():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('addParty.html',{'display':'none'})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/addparty', methods=['POST'])
def addPartyDB():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            _party_type = request.form.get('type')
            _party_name = request.form.get('party').strip().upper()
            _balance = request.form.get('balance')

            if(not checkPartyItemExists(_party_name, _party_type)):
                address = ''
                if(request.form.get('address')):
                    address = request.form.get('address')
                if(_party_type == 'debtor'):
                    party_id = getNewID('debtor_id')
                    table = debtorsTable
                    _id = 'debtor_id'
                else:
                    party_id = getNewID('creditor_id')
                    table = creditorsTable
                    _id = 'creditor_id'

                columns = "{},name,address,balance".format(_id)
                values = "'{}','{}','{}',{}".format(party_id,_party_name,address,_balance)
                insertData(table, columns,values)
                return showWebPage('addParty.html',{'error':'Party added', 'display':'true'})

            else:
                e= {'error':'Party Already Exists', 'display':'true'}
            
                return showWebPage('addParty.html',e)
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/payment')
def payment():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:

            creditorsData = getData(creditorsTable,'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown",'Select Party Name', 1, 0)
            
            return showWebPage('payment.html', {'creditors':creditorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/payment', methods=['POST'])
def enterPayment():
    if(session.get('user_id')):
        if(session.get('access_group') == 'all_access'):
            try:
                _creditor_id = request.form.get('creditor')
                _amount = request.form.get('amount')
                _bill_date = request.form.get('billDate')
                
                narration = ''
                if(request.form.get('narration')):
                    narration = request.form.get('narration')

                bill_no = getNewID('bill_no')
             # c.execute('''CREATE TABLE INVOICE
             # (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')
                columns='bill_no, party_id, narration, total_amt, type, bill_date'
                values = "'{}', '{}', '{}', '{}', '{}', '{}'".format(bill_no, _creditor_id, narration, _amount, "payment", _bill_date)

                insertData('invoice',columns, values)
                updateBalance("creditor",_creditor_id,_amount,"sub")
                return redirect('/payment')

            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return showWebPage('404.html',{'error' :"no access"})   
    else:
        redirect('/')


@app.route('/receipt')
def receipt():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            
            debtorsData = getData(debtorsTable,'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown",'Select Party Name', 1, 0)
            
            return showWebPage('receipt.html', {'debtors':debtorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/receipt', methods=['POST'])
def enterReceipt():
    if(session.get('user_id')):
        if(session.get('access_group') == 'all_access'):
            try:
                _debtor_id = request.form.get('debtor')
                _amount = request.form.get('amount')
                _bill_date = request.form.get('billDate')
                
                narration = ''
                if(request.form.get('narration')):
                    narration = request.form.get('narration')

                bill_no = getNewID('bill_no')
             # c.execute('''CREATE TABLE INVOICE
             # (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')
                columns='bill_no, party_id, narration, total_amt, type, bill_date'
                values = "'{}', '{}', '{}', '{}', '{}', '{}'".format(bill_no, _debtor_id, narration, _amount, "receipt", _bill_date)

                insertData('invoice',columns, values)
                updateBalance("debtor",_debtor_id,_amount,"sub")
                return redirect('/receipt')

            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return showWebPage('404.html',{'error' :"no access"})   
    else:
        redirect('/')

@app.route('/sales')
def sales():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id')
            itemDropDown = createDropDown(itemData, 'item1', 'Select Item', 1, 0,"class ='itemDropDown'")

            debtorsData = getData(debtorsTable,'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown",'Select Party Name', 1, 0)
            
            return showWebPage('sales.html', {'items':itemDropDown, 'debtors':debtorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/sales', methods=['POST'])
def enterSales():
    if(session.get('user_id')):
        if(session.get('access_group') == 'all_access'):
            try:
                _debtor_id = request.form.get('debtor')
                _item_all = getAllElements('item')
                _quantity_all = getAllElements('quantity')
                _rate_all = getAllElements('rate')
                _amount_all = getAllElements('amount')
                _bill_date = request.form.get('billDate')

                totalAmount = request.form.get('totalAmount')
                narration = ''
                if(request.form.get('narration')):
                    narration = request.form.get('narration')

                bill_no = getNewID('bill_no')
                columns='bill_no, party_id, narration, total_amt, type, bill_date'
                values = "'{}', '{}', '{}', '{}', '{}', '{}'".format(bill_no, _debtor_id, narration, totalAmount, "sales", _bill_date)

                insertData('invoice',columns, values)
                insertInvoiceDetails(bill_no,_item_all,_quantity_all,_rate_all,_amount_all,'sales',_bill_date)
                updateBalance("debtor",_debtor_id,totalAmount,"add")
                return redirect('/sales')

            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return showWebPage('404.html',{'error' :"no access"})   
    else:
        redirect('/')


@app.route('/purchase')
def purchase():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id')
            itemDropDown = createDropDown(itemData, 'item1', 'Select Item', 1, 0,"class ='itemDropDown'")

            creditorsData = getData(creditorsTable,'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown",'Select Party Name', 1, 0)
            
            return showWebPage('purchase.html', {'items':itemDropDown, 'creditors':creditorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})

@app.route('/purchase', methods=['POST'])
def enterPurchase():
    if(session.get('user_id')):
        if(session.get('access_group') == 'all_access'):
            try:
                _creditor_id = request.form.get('creditor')
                _item_all = getAllElements('item')
                _quantity_all = getAllElements('quantity')
                _rate_all = getAllElements('rate')
                _amount_all = getAllElements('amount')
                _bill_date = request.form.get('billDate')

                totalAmount = request.form.get('totalAmount')
                narration = ''
                if(request.form.get('narration')):
                    narration = request.form.get('narration')

                bill_no = getNewID('bill_no')
                columns='bill_no, party_id, narration, total_amt, type, bill_date'
                values = "'{}', '{}', '{}', '{}', '{}', '{}'".format(bill_no, _creditor_id, narration, totalAmount, "purchase", _bill_date)

                insertData('invoice',columns, values)
                insertInvoiceDetails(bill_no,_item_all,_quantity_all,_rate_all,_amount_all,'purchase',_bill_date)
                updateBalance("creditor",_creditor_id,totalAmount,"add")
                return redirect('/purchase')

            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return showWebPage('404.html',{'error' :"no access"})   
    else:
        redirect('/')

@app.route('/receive')
def receive():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id')
            itemDropDown = createDropDown(itemData, 'item', 'Select Item', 1, 0)

            creditorsData = getData(creditorsTable,'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, 'creditor','Select Party Name', 1, 0)
            
            return showWebPage('receive.html', {'items':itemDropDown, 'creditors':creditorsDropDown})
        except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return showWebPage('404.html',{'error' :"no access"})


@app.route('/receive', methods=['POST'])
def enterReceive():
    try:
        _item_id = request.form.get('item')
        _creditor_id = request.form.get('creditor')
        _quantity = request.form.get('quantity')
        _receipt_date = request.form.get('receipt_date')
        
        receipt_id = getNewID('receipt_id')
        if(request.form.get('vehicle_no')):
            _vehicle_no=request.form.get('vehicle_no')
            columns='receipt_id, item_id, qty,receipt_date, creditor_id, vehicle_no'
            values = "'{}', '{}', '{}', '{}', '{}'".format(receipt_id, _item_id, _quantity, str(_receipt_date), _creditor_id, _vehicle_no)
        else:
            columns='receipt_id, item_id, qty,receipt_date, creditor_id'
            values = "'{}', '{}', '{}', '{}', '{}'".format(receipt_id, _item_id, _quantity, str(_receipt_date), _creditor_id)
        insertData('received',columns, values)
        return redirect('/receive')

    except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return redirect('/receive')



@app.route('/login')
def showSignUp():
    if(session.get('user_id')):
        return redirect('/')
    else:
        return showWebPage('login.html',{})

@app.route('/login',methods=['POST'])
def validateLogin():
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _email = request.form.get('inputEmail')
        _password = request.form.get('inputPassword')
       # captcha_response = request.form.get('g-recaptcha-response')
        print(_email+" "+_password)
        # validate the received values
        if _email and _password:

            
            # All Good, let's call MySQL
            #validate captcha from api
            #r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':captcha_secret_key ,'response':captcha_response})
            #is_success_captcha = r.json()['success']
            try:
                # data = cursor.callproc('validate_login_inquizitive',(_email, _password))
                data = cursor.execute('select * from app_users where email="'+_email+'" and password="'+_password+'"')
                data = cursor.fetchall()
                # if len(data) > 0:
                    # conn.commit()
                if len(data) > 0:
                    conn.commit()
                    session['user_id'] = str(data[0][0])
                    session['name'] = str(data[0][1])
                    session['email'] = str(data[0][2])
                    session['access_group'] = str(data[0][4])
                    return redirect('/')
                else:
                    print 'not validated'
                    return showWebPage('login.html', {'error':"not validated"})
            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return showWebPage('404.html',{'error': "Enter all the values. Please :("})

    except Exception as e:
        return json.dumps({'errory':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route("/get/bal")
def getBal():
    _id = request.args.get('id', 0)
    _type = request.args.get('type', 0)
    if(_type == 'debtor'):
        currBal = getData(debtorsTable, 'balance', "debtor_id = '{}'".format(_id))[0][0]
    else:
        currBal = getData(creditorsTable, 'balance', "creditor_id = '{}'".format(_id))[0][0]
    print currBal
    return jsonify({
        "currBal"        :  currBal,
    })

@app.route("/get/qty")
def getQty():
    _id = request.args.get('id', 0)
    currQty = getData(itemsTable, 'curr_qty', "item_id = '{}'".format(_id))[0][0]
    print currQty
    return jsonify({
        "currQty"        :  currQty,
    })

@app.route("/get/parties")
def getParties():
    _type = request.args.get('type', 0)
    print "abcd"
    if(_type == 'debtor'):
        debtorsData = getData(debtorsTable,'name, debtor_id')
        dropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown",'Select Party Name', 1, 0)
    else:
        creditorsData = getData(creditorsTable,'name, creditor_id')
        dropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown",'Select Party Name', 1, 0)
    print dropDown
    return jsonify({
        "dropDown"        :  dropDown,
    })

@app.route("/get/bill/details")
def getBillDetails():
    _id = request.args.get('id', 0)
    # (bill_no text, item_id text, qty real, rate real, amount real, foreign key(bill_no) REFERENCES invoice(bill_no))''')

    data = getData('INVOICE_DETAILS natural join items','items.name, qty, rate, amount',"bill_no='{}'".format(_id))
    print data



    itemDetails = createBillDetailsRow(data,['item_id','qty','rate','amount'],[0,1,2,3])
    print itemDetails
    return jsonify({
        "itemDetails"        :  itemDetails,
    })
    

@app.route("/get/party/details")
def getPartyDetails():
    _id = request.args.get('id', 0)
    _type = request.args.get('type', 0)
             # (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')

    data = getData('INVOICE','bill_no, narration, total_amt, bill_date, type',"party_id='{}'".format(_id))
    print data

    tbody = createBillsTable(data,['bill_no', 'narration', 'total_amt', 'bill_date', 'type'],[0,3,2],4)
    print tbody
    return jsonify({
        "tbody"        :  tbody,
    })
    


def getAllElements(prefixString):
    listValues = []
    i=1
    print(prefixString+str(i))
    while True:
        if(request.form.get(prefixString+str(i))):
            listValues.append(str(request.form.get(prefixString+str(i))))
            i+=1
        else:
            break
    return listValues


def showWebPage(page, vars):
    vars['namex'] = session.get('name')
    return render_template(page,vars=vars)

def createBillDetailsRow(data,columns,indexes):
    # data,['item_id','qty','rate','amount',],[0,3,2],4):
    i=0
    trow=[]
    for row in data:
        trow.append('<td></td>')
        for index in indexes:
            if(columns[index]=='amount'):
                trow[i]+="<td>{}</td>".format(locale.currency(float(row[index]),grouping=True,symbol=False))
            else:
                trow[i]+="<td>{}</td>".format(row[index])
        i+=1
        
    return trow


def createBillsTable(data,columns, indexes,type_index):
    tbody=''
    i=1
    debt_sum=0.0
    cred_sum=0.0
    for row in data:
        bill_id=row[indexes[0]]
        bill_no='bill'+str(i)
        tbody+="<tr id='"+bill_no+"' class='bill'> "
        tbody+='<td><a onclick="getBilldata(\'{}\')"><i class="mdi mdi-arrow-down">expand</a></td>'.format(bill_id)
        for index in indexes:
            if(columns[index] =='total_amt' and (row[type_index] == 'receipt' or row[type_index] == 'purchase')):
                cred_sum+= float(row[index])
                tbody+="<td></td>"
                tbody+="<td>"+locale.currency(float(row[index]),grouping=True,symbol=False)+"</td>"
            elif(columns[index] == 'total_amt'):
                debt_sum+=float(row[index])
                tbody+="<td>"+locale.currency(float(row[index]),grouping=True,symbol=False)+"</td>"
                tbody+="<td></td>"
            else:
                tbody+="<td>"+str(row[index])+"</td>"
        tbody+="<td><a><i class='mdi mdi-border-color' onclick='editBill(\""+row[0]+"\")'>Edit</td></a>"
        tbody+="</tr>\
        <tr style='display: none;' class='{}-toggle billDetailHead'>\
        <th></th>\
        <th>Item</th>\
        <th>Quantity</th>\
        <th>Rate</th>\
        <th>Total</th>\
        </tr><tr style='display: none;' class='{}-toggle billDetail' id='{}-details'></tr>".format(bill_id,bill_id,bill_id)

        # <div class="collapse" id="invoice">
        #         <ul class="nav flex-column sub-menu">
        #           <li class="nav-item">
        #             <a class="nav-link" href="/sales">
        #               <span class="menu-title">Sales</span>
        #               <i class="mdi mdi-format-list-bulleted menu-icon"></i>
        #             </a>
        #           </li>
        i+=1
    tbody+="<tr id='totals' style='font-weight: bold;'><td>Total</td><td></td><td></td><td>"+locale.currency(float(debt_sum),grouping=True,symbol=False)+"</td><td>"+locale.currency(float(cred_sum),grouping=True,symbol=False)+"</td></tr>"
    bal = debt_sum-cred_sum
    if(bal>=0):
        tbody+="<tr id='balance' style='font-weight: bold;'> <td>Balance</td><td></td><td></td><td>{}</td><td></td>".format(locale.currency(float(bal),grouping=True,symbol=False))
    else:
        tbody+="<tr id='balance' style='font-weight: bold;'> <td>Balance</td><td></td><td></td><td></td><td>{}</td>".format(locale.currency(float(-bal),grouping=True,symbol=False))
    return tbody


def checkPartyItemExists(_party_name, _type):
    if(_type == 'debtor'):
        table = debtorsTable
    elif(_type == 'item'):
        table='items'
    else:
        table = creditorsTable
    data = getData(table, '*', "name='{}'".format(_party_name))
    print data
    if(len(data)==0):
        return False
    else:
        return True

def createDropDown(data, dropDownName, defaultOption, valueIndex, nameIndex,className="class='form-control'"):
    dropDown = "<select name='"+dropDownName+"'"+ className +" required> "
    dropDown += "<option selected='selected' disabled='disabled'>"+defaultOption+"</option>"
    for row in data:
        dropDown += "<option value='" + str(row[valueIndex]) + "'> " + str(row[nameIndex]) + "</option>"
    dropDown +="</select>"
    return dropDown







# c.execute('''CREATE TABLE daily_inventory
             # (ITEM_ID text, Qty real, date text, PRIMARY KEY ('ITEM_id'), FOREIGN KEY(item_id) REFERENCES items(item_id))''')





@app.errorhandler(404)
def page_not_found(e):
    return showWebPage('404.html', {'error':"The page you requested was not found!"})

if __name__ == "__main__":
    app.run(debug=True,port=10003,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
