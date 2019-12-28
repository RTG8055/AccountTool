import requests

import datetime

from flask import Flask, render_template, redirect, json, request, session, Markup, flash
import sqlite3

app = Flask(__name__)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 

databaseName = 'example2.db'
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
        print _dispatch_date
        insertData('dispatch','item_id, qty,dispatch_date, debtor_id',"{}, {}, '{}', {}".format(_item_id, _quantity, str(_dispatch_date), _debtor_id))
    except Exception as e:
            return json.dumps({'errory':str(e)})
    else:
        return redirect('/dispatch')

# @app.route('/dispatch')
# def entry():
#     if(session.get('user_id') and session.get('access_group') == 'all_access'):


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
        print _receipt_date
        insertData('received','item_id, qty,receipt_date, creditor_id',"{}, {}, '{}', {}".format(_item_id, _quantity, str(_receipt_date), _creditor_id))
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


def showWebPage(page, vars):
    vars['namex'] = session.get('name')
    return render_template(page,vars=vars)


def getData(table, columns='*'):
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    data = cursor.execute("select "+columns+ " from "+table)
    data = cursor.fetchall()
    return data

def createDropDown(data, dropDownName, defaultOption, valueIndex, nameIndex):
    dropDown = "<select name='"+dropDownName+"' class='form-control'> "
    dropDown += "<option selected='selected' disabled='disabled'>"+defaultOption+"</option>"
    for row in data:
        dropDown += "<option value='" + str(row[valueIndex]) + "'> " + str(row[nameIndex]) + "</option>"
    dropDown +="</select>"
    return dropDown

def insertData(table, columns, values):
    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    print("insert into {}({}) values ({})".format(table, columns, values))
    data = cursor.execute("insert into {} ({}) values ({})".format(table, columns, values))
    print data.fetchall()
    conn.commit()
    return data

def updateInventory(table, item_id):
    conn = sqlite3.connect(databaseName)
    cursor = conn.cursor()
    data = cursor.execute("select * from "+table)



@app.errorhandler(404)
def page_not_found(e):
    return showWebPage('404.html', {'error':"The page you requested was not found!"})

if __name__ == "__main__":
    app.run(debug=True,port=10003,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
