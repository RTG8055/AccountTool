import locale
import os
import sqlite3
from datetime import date
import datetime

from flask import Flask, render_template, redirect, json, request, session, jsonify

from DBUtilsAWS import *

locale.setlocale(locale.LC_ALL, '')

app = Flask(__name__)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92'

databaseName = 'example6.db'
itemsTable = 'items'
debtorsTable = 'debtors'
creditorsTable = 'creditors'
usersTable = 'app_users'
access_groups = []

insert_dispatch = 'insert_dispatch'
insert_receive = 'insert_receive'
insert_debtor = 'insert_debtor'
insert_creditor = 'insert_creditor'
insert_invoice = 'insert_invoice'
insert_invoice_details = 'insert_invoice_details'
insert_item = 'insert_item'
insert_user = 'insert_user'
update_invoice = 'update_invoice'


@app.route('/')
@app.route('/home')
def main():
    if (session.get('user_id')):
        return showWebPage('home.html', {'namex': session.get('name')})
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dispatch')
def dispatch():
    if session.get('user_id') and session.get('access_group') == 'all_access':
        try:
            itemData = getData(itemsTable, 'name, item_id', extra='order by name')
            itemDropDown = createDropDown(itemData, 'item', 'Select Item', 1, 0)

            debtorsData = getData(debtorsTable, 'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, 'debtor', 'Select Party Name', 1, 0)

            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get('billDate')
            return showWebPage('dispatch.html',
                               {'items': itemDropDown, 'debtors': debtorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/dispatch', methods=['POST'])
def enterDispatch():
    try:
        _item_id = request.form.get('item')
        _debtor_id = request.form.get('debtor')
        _quantity = request.form.get('quantity')
        _dispatch_date = request.form.get('dispatch_date')

        if (request.form.get('vehicle_no')):
            _vehicle_no = request.form.get('vehicle_no')
        else:
            _vehicle_no = ''

        values = [_item_id, _quantity, datetime.datetime.strptime(_dispatch_date,"%d/%m/%Y"),_debtor_id, _vehicle_no]
        print("dipatch:",call_procedure(insert_dispatch, values))
    except Exception as e:
        return json.dumps({'errory': str(e)})
    else:
        return redirect('/dispatch')


@app.route('/receive')
def receive():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id', extra='order by name')
            itemDropDown = createDropDown(itemData, 'item', 'Select Item', 1, 0)

            creditorsData = getData(creditorsTable, 'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, 'creditor', 'Select Party Name', 1, 0)

            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get('billDate')
            return showWebPage('receive.html',
                               {'items': itemDropDown, 'creditors': creditorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/receive', methods=['POST'])
def enterReceive():
    try:
        _item_id = request.form.get('item')
        _creditor_id = request.form.get('creditor')
        _quantity = request.form.get('quantity')
        _receipt_date = request.form.get('receipt_date')

        if (request.form.get('vehicle_no')):
            _vehicle_no = request.form.get('vehicle_no')
        else:
            _vehicle_no = ''

        values = [_item_id, _quantity, datetime.datetime.strptime(_receipt_date,"%d/%m/%Y"),_creditor_id, _vehicle_no]
        call_procedure(insert_receive, values)
        session['billDate'] = _receipt_date
        return redirect('/receive')

    except Exception as e:
        return json.dumps({'errory': str(e)})


@app.route('/viewpartybills')
def viewPartyBills():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('viewParties.html', {})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


#
# @app.route('/viewpartybills', methods=['GET', 'POST'])
# def viewPartyBillsReq():
#     if (session.get('user_id') and session.get('access_group') == 'all_access'):
#         try:
#             return showWebPage('viewParties.html', {})
#         except Exception as e:
#             return json.dumps({'errory': str(e)})
#     else:
#         return showWebPage('404.html', {'error': "no access"})


@app.route('/additem')
def additem():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('addItem.html', {'display': 'none'})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/additem', methods=['POST'])
def addItemDB():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:

            _item_name = request.form.get('item').strip().upper()
            _qty = request.form.get('qty')

            if (not checkPartyItemExists(_item_name, 'item')):
                address = ''
                values = [_item_name, address, _qty]
                call_procedure(insert_item, values)
                return showWebPage('addItem.html', {'error': 'Item Added', 'display': 'true'})

            else:
                e = {'error': 'Item Already Exists', 'display': 'true'}

                return showWebPage('addItem.html', e)
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/addparty')
def addParty():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            return showWebPage('addParty.html', {'display': 'none'})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/addparty', methods=['POST'])
def addPartyDB():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            _party_type = request.form.get('type')
            _party_name = request.form.get('party').strip().upper()
            _balance = request.form.get('balance')

            if (not checkPartyItemExists(_party_name, _party_type)):
                address = ''
                insert_procedure = ''
                if (request.form.get('address')):
                    address = request.form.get('address')
                if (_party_type == 'debtor'):
                    insert_procedure = insert_debtor
                else:
                    insert_procedure = insert_creditor
                values = [_party_name, address, _balance]
                call_procedure(insert_procedure, values)
                return showWebPage('addParty.html', {'error': 'Party added', 'display': 'true'})

            else:
                e = {'error': 'Party Already Exists', 'display': 'true'}

                return showWebPage('addParty.html', e)
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/payment')
def payment():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:

            creditorsData = getData(creditorsTable, 'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown", 'Select Party Name', 1,
                                               0)
            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get(
                'billDate')
            return showWebPage('payment.html', {'creditors': creditorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/payment', methods=['POST'])
def enterPayment():
    if (session.get('user_id')):
        if (session.get('access_group') == 'all_access'):
            try:
                _creditor_id = request.form.get('creditor')
                _amount = request.form.get('amount')
                _bill_date = request.form.get('billDate')
                narration = ''
                if (request.form.get('narration')):
                    narration = request.form.get('narration')
                values = [_creditor_id, narration, _amount, "payment",datetime.datetime.strptime(_bill_date,"%d/%m/%Y")]
                call_procedure(insert_invoice, values)
                session['billDate'] = _bill_date
                return redirect('/payment')
            except Exception as e:
                return json.dumps({'errory': str(e)})
        else:
            return showWebPage('404.html', {'error': "no access"})
    else:
        redirect('/')


@app.route('/receipt')
def receipt():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            debtorsData = getData(debtorsTable, 'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown", 'Select Party Name', 1, 0)
            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get('billDate')
            return showWebPage('receipt.html', {'debtors': debtorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/receipt', methods=['POST'])
def enterReceipt():
    if (session.get('user_id')):
        if (session.get('access_group') == 'all_access'):
            try:
                _debtor_id = request.form.get('debtor')
                _amount = request.form.get('amount')
                _bill_date = request.form.get('billDate')
                narration = ''
                if (request.form.get('narration')):
                    narration = request.form.get('narration')
                values = [_debtor_id, narration, _amount, "receipt",datetime.datetime.strptime(_bill_date,"%d/%m/%Y")]
                call_procedure(insert_invoice, values)
                session['billDate'] = _bill_date
                return redirect('/receipt')
            except Exception as e:
                return json.dumps({'errory': str(e)})
        else:
            return showWebPage('404.html', {'error': "no access"})
    else:
        redirect('/')


@app.route('/sales')
def sales():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            # print("date: ", billDate)
            itemData = getData(itemsTable, 'name, item_id', extra='order by name')
            itemDropDown = createDropDown(itemData, 'item1', 'Select Item', 1, 0,
                                          "class ='itemDropDown")

            debtorsData = getData(debtorsTable, 'name, debtor_id')
            debtorsDropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown", 'Select Party Name', 1, 0)
            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get('billDate')
            return showWebPage('sales.html', {'items': itemDropDown, 'debtors': debtorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/sales', methods=['POST'])
def enterSales():
    if (session.get('user_id')):
        if (session.get('access_group') == 'all_access'):
            try:
                _debtor_id = request.form.get('debtor')
                _item_all = getAllElements('item')
                _quantity_all = getAllElements('quantity')
                _rate_all = getAllElements('rate')
                _amount_all = getAllElements('amount')
                _bill_date = request.form.get('billDate')

                totalAmount = request.form.get('totalAmount')
                narration = ''
                if (request.form.get('narration')):
                    narration = request.form.get('narration')

                invoiceValues = [_debtor_id, narration, totalAmount,"sales",datetime.datetime.strptime(_bill_date,"%d/%m/%Y")]

                call_procedure(insert_invoice, invoiceValues)
                bill_no = getData('invoice', 'max(bill_no)', "party_id='{}' and type='{}' and total_amt={} and bill_date='{}'".format(_debtor_id, "sales", totalAmount,datetime.datetime.strptime(_bill_date,"%d/%m/%Y")))
                insertInvoiceDetails(bill_no, _item_all, _quantity_all, _rate_all, _amount_all, 'sales', datetime.datetime.strptime(_bill_date,"%d/%m/%Y"))
                session['billDate'] = _bill_date
                return redirect('/sales')
            except Exception as e:
                return json.dumps({'errory': str(e)})
        else:
            return showWebPage('404.html', {'error': "no access"})
    else:
        redirect('/')


@app.route('/purchase')
def purchase():
    if (session.get('user_id') and session.get('access_group') == 'all_access'):
        try:
            itemData = getData(itemsTable, 'name, item_id', extra='order by name')
            itemDropDown = createDropDown(itemData, 'item1', 'Select Item', 1, 0,
                                          "class ='itemDropDown")

            creditorsData = getData(creditorsTable, 'name, creditor_id')
            creditorsDropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown", 'Select Party Name', 1,
                                               0)
            billDate = date.today().strftime("%d/%m/%Y") if session.get('billDate') is None else session.get('billDate')
            return showWebPage('purchase.html',
                               {'items': itemDropDown, 'creditors': creditorsDropDown, 'billDate': billDate})
        except Exception as e:
            return json.dumps({'errory': str(e)})
    else:
        return showWebPage('404.html', {'error': "no access"})


@app.route('/purchase', methods=['POST'])
def enterPurchase():
    if (session.get('user_id')):
        if (session.get('access_group') == 'all_access'):
            try:
                _creditor_id = request.form.get('creditor')
                _item_all = getAllElements('item')
                _quantity_all = getAllElements('quantity')
                _rate_all = getAllElements('rate')
                _amount_all = getAllElements('amount')
                _bill_date = request.form.get('billDate')

                totalAmount = request.form.get('totalAmount')
                narration = ''
                if (request.form.get('narration')):
                    narration = request.form.get('narration')

                invoiceValues = [_creditor_id, narration, totalAmount,"purchase", datetime.datetime.strptime(_bill_date,"%d/%m/%Y")]

                call_procedure(insert_invoice, invoiceValues)
                bill_no = getData('invoice', 'max(bill_no)', "party_id='{}' and type='{}' and total_amt={} and bill_date='{}'".format(_creditor_id, "purchase", totalAmount,datetime.datetime.strptime(_bill_date,"%d/%m/%Y")))
                insertInvoiceDetails(bill_no, _item_all, _quantity_all, _rate_all, _amount_all, 'purchase', datetime.datetime.strptime(_bill_date,"%d/%m/%Y"))
                session['billDate'] = _bill_date
                return redirect('/purchase')

            except Exception as e:
                return json.dumps({'errory': str(e)})
        else:
            return showWebPage('404.html', {'error': "no access"})
    else:
        redirect('/')


@app.route('/editbillPayment', methods=['GET', 'POST'])
def editBillDB():
    if (session.get('user_id')):

        billno = request.args.get('billNo', 0)
        billType = request.args.get('billType', 0)

        print("inside editBIll:", billno)
        _party_id=''
        if(billType == 'receipt' or billType == 'sales'):
            _party_id = request.form.get('debtor')
        elif (billType == 'payment' or billType == 'purchase'):
            _party_id = request.form.get('creditor')

        totalAmount = request.form.get('totalAmount')
        narration = ''
        _bill_date = request.form.get('billDate')
        if (request.form.get('narration')):
            narration = request.form.get('narration')
        if (billType == 'sales' or billType == 'purchase'):
            old_item_nos = int(request.args.get('itemNo', 0))
            _item_all = getAllElements('item')
            _quantity_all = getAllElements('quantity')
            _rate_all = getAllElements('rate')
            _amount_all = getAllElements('amount')
            _bill_detail_all = getAllElements('billDetailId')
            if (old_item_nos > len(_item_all)):
                return redirect('/error404')
            updateInvoiceDetails(billno, _item_all, _quantity_all, _rate_all, _amount_all,_bill_detail_all, 'purchase',
                                 datetime.datetime.strptime(_bill_date, "%d/%m/%Y"),old_item_nos)

        invoiceValues = [billno, _party_id, narration, totalAmount, datetime.datetime.strptime(_bill_date, "%d/%m/%Y")]
        call_procedure(update_invoice, invoiceValues)
        return redirect('/' + billType)
    else:
        return redirect('/')


@app.route('/editbill/<billno>/<partyType>/<billType>')
def editBill(billno, partyType, billType):
    if (session.get('user_id')):
        print("inside editBIll:", billno)

        invoiceData = \
            getData('invoice', "party_id, narration, total_amt, bill_date, type", "bill_no ='{}'".format(billno))[0]
        print(invoiceData)

        itemData = getData(itemsTable, 'name, item_id', extra='order by name')
        itemDropDown = createDropDown(itemData, 'item1', 'Select Item', 1, 0,
                                      "class ='itemDropDown")
        selectedPartyId = invoiceData[0]
        selectedBillNarration = invoiceData[1]
        selectedBillAmount = invoiceData[2]
        selectedBillDate = invoiceData[3].strftime("%d/%m/%Y")
        if (partyType == 'debtor'):
            debtorsData = getData(debtorsTable, 'name, debtor_id')
            selectedPartyName = getData(debtorsTable, 'name', "debtor_id='{}'".format(selectedPartyId))[0][0]
            debtorsDropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown", 'Select Party Name', 1, 0,
                                             selected=selectedPartyName)
            parties = debtorsDropDown
        else:
            creditorsData = getData(creditorsTable, 'name, creditor_id')
            selectedPartyName = getData(creditorsTable, 'name', "creditor_id='{}'".format(selectedPartyId))[0][0]
            creditorsDropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown", 'Select Party Name',
                                               1,
                                               0, selected=selectedPartyName)
            parties = creditorsDropDown
        if (billType == 'receipt' or billType == 'payment'):
            return showWebPage('editBillPayment.html',
                               {'billDate': selectedBillDate, 'billNo': billno, 'billType': billType,
                                'prevAmt': selectedBillAmount, 'partyList': parties, 'narration': selectedBillNarration})


        invoiceDetailsData = getData('invoice_details natural join items', 'items.name, qty, rate, amount, bill_detail_id',
                                     "bill_no='{}'".format(billno))
        totalAmt = 0
        for i in invoiceDetailsData:
            totalAmt += i[3]
        print(invoiceDetailsData)
        numberOfItems = len(invoiceDetailsData)
        print(numberOfItems)
        billItemData = createEditInventoryBillTable(invoiceDetailsData, itemData)

        return showWebPage('editBill.html',
                           {'billDate': selectedBillDate, 'billNo': billno, 'billType': billType, 'itemNo': numberOfItems,
                            'partyName': selectedPartyName, 'items': itemDropDown, 'partyList': parties,
                            'billItemData': billItemData, 'totalAmt': totalAmt, 'narration': selectedBillNarration})
    else:
        return redirect('/')


@app.route('/login')
def showSignUp():
    if (session.get('user_id')):
        return redirect('/')
    else:
        return render_template('login.html', vars={})


@app.route('/login', methods=['POST'])
def validateLogin():
    print(os.getcwd())
    print(os.path.realpath(databaseName))
    # conn = sqlite3.connect("C:\\Users\\rahagaga\\Documents\\Rahul\\github\\AccountTool\\example6.db")
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _email = request.form.get('inputEmail')
        _password = request.form.get('inputPassword')
        # captcha_response = request.form.get('g-recaptcha-response')
        print(_email + " " + _password)
        # validate the received values
        # conn = sqlite3.connect(os.path.realpath(databaseName))
        if _email and _password:

            # All Good, let's call MySQL
            # validate captcha from api
            # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':captcha_secret_key ,'response':captcha_response})
            # is_success_captcha = r.json()['success']
            try:
                # data = cursor.callproc('validate_login_inquizitive',(_email, _password))
                data = cursor.execute(
                    'select * from app_users where email="' + _email + '" and password="' + _password + '"')
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
                    print('not validated')
                    return showWebPage('login.html', {'error': "not validated"})
            except Exception as e:
                return json.dumps({'errory': str(e)})
        else:
            return showWebPage('404.html', {'error': "Enter all the values. Please :("})

    except Exception as e:
        return json.dumps({'errory': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route("/get/bal")
def getBal():
    _id = request.args.get('id', 0)
    _type = request.args.get('type', 0)
    if (_type == 'debtor'):
        currBal = getData(debtorsTable, 'balance', "debtor_id = '{}'".format(_id))[0][0]
    else:
        currBal = getData(creditorsTable, 'balance', "creditor_id = '{}'".format(_id))[0][0]
    print(currBal)
    return jsonify({
        "currBal": currBal,
    })


@app.route("/get/qty")
def getQty():
    _id = request.args.get('id', 0)
    currQty = getData(itemsTable, 'curr_qty', "item_id = '{}'".format(_id))[0][0]
    print(currQty)
    return jsonify({
        "currQty": currQty,
    })


@app.route("/get/parties")
def getParties():
    _type = request.args.get('type', 0)
    if (_type == 'debtor'):
        debtorsData = getData(debtorsTable, 'name, debtor_id')
        dropDown = createDropDown(debtorsData, "debtor' id='debtorDropDown", 'Select Party Name', 1, 0)
    else:
        creditorsData = getData(creditorsTable, 'name, creditor_id')
        dropDown = createDropDown(creditorsData, "creditor' id='creditorDropDown", 'Select Party Name', 1, 0)
    print(dropDown)
    return jsonify({
        "dropDown": dropDown,
    })


@app.route("/get/bill/details")
def getBillDetails():
    _id = request.args.get('id', 0)
    # (bill_no text, item_id text, qty real, rate real, amount real, foreign key(bill_no) REFERENCES invoice(bill_no))''')

    data = getData('invoice_details natural join items', 'items.name, qty, rate, amount', "bill_no='{}'".format(_id))
    print(data)

    itemDetails = createBillDetailsRow(data, ['item_id', 'qty', 'rate', 'amount'], [0, 1, 2, 3])
    print(itemDetails)
    return jsonify({
        "itemDetails": itemDetails,
    })


@app.route("/get/party/billsPDF")
def getPartyDetailsPDF():
    _id = request.args.get('id', 0)
    _type = request.args.get('type', 0)
    _from = request.args.get('from', 0)
    _to = request.args.get('to', 0)
    FILTER = ''
    if (_from != "9999"):
        FILTER += "and bill_date > '{}'".format(datetime.datetime.strptime(_from,"%d/%m/%Y"))
    if (_to != "9999"):
        FILTER += "and bill_date < '{}'".format(datetime.datetime.strptime(_to,"%d/%m/%Y"))
        # (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')

    print("to and from : ", datetime.datetime.strptime(_to,"%d/%m/%Y"), datetime.datetime.strptime(_from,"%d/%m/%Y"))
    data = getData('invoice', "bill_no, narration, total_amt, bill_date, type", "party_id ='{}' {}".format(_id, FILTER),
                   " order by bill_date")
    print(data)
    # fig, ax = plt.subplots()
    # fig.patch.set_visible(False)
    # ax.axis('off')
    # ax.axis('tight')
    # df = pd.DataFrame(data, columns=['bill_no', 'narration', 'total_amt', 'bill_date', 'type'])
    # ax.table(cellText=df.values, colLabels=df.columns, loc='center')
    # fig.tight_layout()
    #
    # plt.show()
    #
    # plt.savefig("table.pdf", bbox_inches='tight')

    tbody = createBillsTablePDF(data, ['bill_no', 'narration', 'total_amt', 'bill_date', 'type'], [0, 3, 2], 4, _type)
    print(tbody)
    return jsonify({
        "tbody": tbody,
    })


@app.route("/get/party/bills")
def getPartyDetails():
    _id = request.args.get('id', 0)
    _type = request.args.get('type', 0)
    _from = request.args.get('from', 0)
    _to = request.args.get('to', 0)
    FILTER = ''
    if (_from != "9999"):
        FILTER += "and bill_date > '{}'".format(datetime.datetime.strptime(_from,"%d/%m/%Y"))
    if (_to != "9999"):
        FILTER += "and bill_date < '{}'".format(datetime.datetime.strptime(_to,"%d/%m/%Y"))
        # (bill_no text, party_id text, narration text, total_amt real, type text,bill_date text)''')

    print("to and from : ", datetime.datetime.strptime(_to,"%d/%m/%Y"), datetime.datetime.strptime(_from,"%d/%m/%Y"))
    data = getData('invoice', "bill_no, narration, total_amt, bill_date, type", "party_id ='{}' {}".format(_id, FILTER),
                   " order by bill_date")
    print(data)

    tbody = createBillsTable(data, ['bill_no', 'narration', 'total_amt', 'bill_date', 'type'], [0, 3, 2], 4, _type)
    print(tbody)
    return jsonify({
        "tbody": tbody,
    })


def getAllElements(prefixString):
    listValues = []
    i = 1
    print(prefixString + str(i))
    while True:
        if (request.form.get(prefixString + str(i))):
            listValues.append(str(request.form.get(prefixString + str(i))))
            i += 1
        else:
            break
    return listValues


def showWebPage(page, vars):
    vars['namex'] = session.get('name')
    return render_template(page, vars=vars)


def createBillDetailsRow(data, columns, indexes):
    # data,['item_id','qty','rate','amount',],[0,3,2],4):
    i = 0
    trow = []
    for row in data:
        trow.append('<td></td>')
        for index in indexes:
            if (columns[index] == 'amount'):
                trow[i] += "<td>{}</td>".format(locale.currency(float(row[index]), grouping=True, symbol=False))
            else:
                trow[i] += "<td>{}</td>".format(row[index])
        i += 1

    return trow


def createEditInventoryBillTable(data, itemData):
    itemRows = ""
    itemNo = 0
    numItems = len(data)
    for item in data:
        itemNo += 1
        itemDropDown = createDropDown(itemData, "item{}".format(itemNo), 'Select Item', 1, 0,
                                      "class ='itemDropDown", selected=item[0])
        row = ""
        row += "<tr id='item{}'>".format(itemNo)
        row += "<td id='sno{}'>".format(itemNo)
        row += "<input name='billDetailId{}' type='text' id='billDetailId{}' placeholder='Bill Detail Id' " \
               "title='BillDetailID' class='billDetailId form-control' value='{}' readonly>".format(itemNo, itemNo, item[4])
        row += "</td>"
        row += "<td id='itemId{}'>{}<p class='card-description' id='currQty{}'></p></td>".format(itemNo, itemDropDown, itemNo)
        row += "<td id='itemQty{}'>".format(itemNo, itemNo)
        row += "<input name='quantity{}' type='number' id='quantity{}' placeholder='Quantity in kGs' class='qty form-control' " \
               "title='Kgs' step='0.01' value='{}' required>".format(itemNo, itemNo, item[1])
        row += "</td>"
        row += "<td id='itemQtyBag{}'>".format(itemNo)
        row += "<input type='number' id='quantityBag{}' placeholder='Quantity in Bags' class='qtyBag form-control' title='Bags' " \
               "step='0.01' value='{}'>".format(itemNo, item[1]/40.0)
        row += "</td>"
        row += "<td id='itemRate{}'>".format(itemNo)
        row += "<input name='rate{}' type='number' id='Rate{}' placeholder='Rate per kG' class='rate form-control' title='Enter " \
               "Rate' step='0.01' value='{}' required>".format(itemNo, itemNo, item[2])
        row += "</td>"
        row += "<td id='itemAmt{}'>".format(itemNo)
        row += "<input name='amount{}' type='number' id='Amount' placeholder='Amount' title='Amount' step='0.01' " \
               "class='Amount form-control' value='{}' readonly>".format(itemNo, item[3])
        row += "</td>"
        row += "<td id='addItem'><i class='mdi mdi-backspace icon-md' style='float:left;' onclick=\"removeItem('{}')\"></i>".format(itemNo)
        if(itemNo==numItems):
            row += "<button id='addButton' class='btn btn-block btn-lg btn-gradient-primary mt-4' onclick=\"addItem('{}');\">+ Add an Item</button>".format(itemNo + 1)
        row += "</td>"
        row += "</tr>"
        itemRows += row
    return itemRows


def createBillsTablePDF(data, columns, indexes, type_index, partyType):
    tbody = '<table><thead><tr><th></th><th>Bill No.</th><th>Bill Date</th><th>Debited Amount</th><th>Credited ' \
            'Amount</th></thead><tbody> '
    i = 1
    debt_sum = 0.0
    cred_sum = 0.0
    for row in data:
        bill_id = row[indexes[0]]
        bill_no = 'bill' + str(i)
        # tbody += "<tbody class='bill-row'>"
        tbody += "<tr id='" + bill_no + "' class='bill'> "
        # tbody += '<td><a onclick="getBilldata(\'{}\')"><i class="mdi mdi-arrow-down">expand</a></td>'.format(bill_id)
        for index in indexes:
            if (columns[index] == 'total_amt' and (row[type_index] == 'receipt' or row[type_index] == 'purchase')):
                cred_sum += float(row[index])
                tbody += "<td></td>"
                tbody += "<td>" + locale.currency(float(row[index]), grouping=True, symbol=False) + "</td>"
            elif (columns[index] == 'total_amt'):
                debt_sum += float(row[index])
                tbody += "<td>" + locale.currency(float(row[index]), grouping=True, symbol=False) + "</td>"
                tbody += "<td></td>"
            else:
                tbody += "<td>" + str(row[index]) + "</td>"
        # tbody += "<td><a href='/editbill/{}/{}'><i class='mdi mdi-border-color'>Edit</td></a>".format(row[0], partyType)

        # tbody += "</tr>\
        #     <tr style='display: none;' class='{}-toggle billDetailHead'>\
        #     <th></th>\
        #     <th>Item</th>\
        #     <th>Quantity</th>\
        #     <th>Rate</th>\
        #     <th>Total</th>\
        #     </tr><tr style='display: none;' class='{}-toggle billDetail' id='{}-details'></tr>".format(bill_id, bill_id,
        #                                                                                                bill_id)
        # tbody += "</tbody>"
        i += 1
    tbody += "<tr id='totals' style='font-weight: bold;' class='billEnd'><td>Total</td><td></td><td></td><td>" + locale.currency(
        float(debt_sum), grouping=True, symbol=False) + "</td><td>" + locale.currency(float(cred_sum), grouping=True,
                                                                                      symbol=False) + "</td></tr>"
    bal = debt_sum - cred_sum
    if (bal >= 0):
        tbody += "<tr id='balance' class='billEnd' style='font-weight: bold;'> <td>Balance</td><td></td><td></td><td>{}</td><td></td>".format(
            locale.currency(float(bal), grouping=True, symbol=False))
    else:
        tbody += "<tr id='balance' class='billEnd' style='font-weight: bold;'> <td>Balance</td><td></td><td></td><td></td><td>{}</td>".format(
            locale.currency(float(-bal), grouping=True, symbol=False))
    tbody += '</tbody>'
    return tbody


def createBillsTable(data, columns, indexes, type_index, partyType):
    tbody = ''
    i = 1
    debt_sum = 0.0
    cred_sum = 0.0
    for row in data:
        bill_id = row[indexes[0]]
        bill_no = 'bill' + str(i)
        # tbody += "<tbody class='bill-row'>"
        tbody += "<tr id='" + bill_no + "' class='bill'> "
        tbody += '<td><a onclick="getBilldata(\'{}\')"><i class="mdi mdi-arrow-down">expand</a></td>'.format(bill_id)
        for index in indexes:
            if (columns[index] == 'total_amt' and (row[type_index] == 'receipt' or row[type_index] == 'purchase')):
                cred_sum += float(row[index])
                tbody += "<td></td>"
                tbody += "<td>" + locale.currency(float(row[index]), grouping=True, symbol=False) + "</td>"
            elif (columns[index] == 'total_amt'):
                debt_sum += float(row[index])
                tbody += "<td>" + locale.currency(float(row[index]), grouping=True, symbol=False) + "</td>"
                tbody += "<td></td>"
            else:
                tbody += "<td>" + str(row[index]) + "</td>"
        tbody += "<td><a href='/editbill/{}/{}/{}'><i class='mdi mdi-border-color'>Edit</td></a>".format(row[0],
                                                                                                         partyType, row[
                                                                                                             type_index])

        tbody += "</tr>\
        <tr style='display: none;' class='{}-toggle billDetailHead'>\
        <th></th>\
        <th>Item</th>\
        <th>Quantity</th>\
        <th>Rate</th>\
        <th>Total</th>\
        </tr><tr style='display: none;' class='{}-toggle billDetail' id='{}-details'></tr>".format(bill_id, bill_id,
                                                                                                   bill_id)
        # tbody += "</tbody>"
        i += 1
    tbody += "<tr id='totals' style='font-weight: bold;' class='billEnd'><td></td><td>Total</td><td></td><td>" + locale.currency(
        float(debt_sum), grouping=True, symbol=False) + "</td><td>" + locale.currency(float(cred_sum), grouping=True,
                                                                                      symbol=False) + "</td></tr>"
    bal = debt_sum - cred_sum
    if (bal >= 0):
        tbody += "<tr id='balance' class='billEnd' style='font-weight: bold;'> <td></td><td>Balance</td><td></td><td>{}</td><td></td>".format(
            locale.currency(float(bal), grouping=True, symbol=False))
    else:
        tbody += "<tr id='balance' class='billEnd' style='font-weight: bold;'> <td></td><td>Balance</td><td></td><td></td><td>{}</td>".format(
            locale.currency(float(-bal), grouping=True, symbol=False))
    return tbody


def checkPartyItemExists(_party_name, _type):
    if (_type == 'debtor'):
        table = debtorsTable
    elif (_type == 'item'):
        table = 'items'
    else:
        table = creditorsTable
    data = getData(table, '*', "name='{}'".format(_party_name))
    print(data)
    if (len(data) == 0):
        return False
    else:
        return True


def createDropDown(data, dropDownName, defaultOption, valueIndex, nameIndex, className="class='form-control",
                   selected='default'):
    className += " js-example-basic-single'"
    dropDown = "<select name='" + dropDownName + "'" + className + " style='width:100%' required> "

    if (selected == 'default'):
        dropDown += "<option selected='selected' disabled='disabled'>" + defaultOption + "</option>"
        i = 0
        for row in data:
            i += 1
            dropDown += "<option value='" + str(row[valueIndex]) + "' data-select2-id='" + str(
                row[valueIndex]) + "'> " + str(row[nameIndex]) + "</option>"
        dropDown += "</select>"
    else:
        for row in data:
            if (row[nameIndex] == selected):
                dropDown += "<option value='" + str(row[valueIndex]) + "' selected> " + str(
                    row[nameIndex]) + "</option>"
            else:
                dropDown += "<option value='" + str(row[valueIndex]) + "' data-select2-id='" + str(
                    valueIndex) + "'> " + str(row[nameIndex]) + "</option>"
        dropDown += "</select>"
    return dropDown


# c.execute('''CREATE TABLE daily_inventory
# (ITEM_ID text, Qty real, date text, PRIMARY KEY ('ITEM_id'), FOREIGN KEY(item_id) REFERENCES items(item_id))''')

@app.route('/error404')
def show_404():
    return showWebPage('404.html', {'error': "The page you requested was not found!"})
@app.errorhandler(404)
def page_not_found(e):
    return showWebPage('404.html', {'error': "The page you requested was not found!"})


if __name__ == "__main__":
    app.run(debug=True, port=10003, use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
