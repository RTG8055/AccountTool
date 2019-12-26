import requests, datetime

from flask import Flask, render_template, redirect, json, request, session, Markup, flash
import sqlite3

app = Flask(__name__)

app.secret_key = '8bf9547569cd5a638931a8639cf9f86237931e92' 
databaseName = 'example3.db'

@app.route('/')
@app.route('/home')
def main():
    if(session.get('user_id')):
        return render_template('home.html', namex=session.get('name'))
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login')
def showSignUp():
    if(session.get('user_id')):
        return redirect('/')
    else:
        return render_template('signin.html')


@app.route('/receive')
def entry():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):
        items = 
        return render_template('receive.html')



@app.route('/dispatch')
def entry():
    if(session.get('user_id') and session.get('access_group') == 'all_access'):





@app.route('/login',methods=['POST'])
def validateLogin():

    conn = sqlite3.connect(databaseName)
    # conn = mysql.connect()
    cursor = conn.cursor()
    try:
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
       # captcha_response = request.form['g-recaptcha-response']
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
                if(_email and _password):
                    session['user_id'] = str(data[0][0])
                    session['name'] = str(data[0][1])
                    session['email'] = str(data[0][2])
                    session['access_group'] = str(data[0][4])
                    return redirect('/')
                else:
                    print 'not validated'
                    return render_template('signin.html', error="not validated")            
            except Exception as e:
                return json.dumps({'errory':str(e)})
        else:
            return render_template('404.html',error = "Enter all the values. Please :(")

    except Exception as e:
        return json.dumps({'errory':str(e)})
    finally:
        cursor.close()
        conn.close()




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error="The page you requested was not found!")

if __name__ == "__main__":
    app.run(debug=True,port=10003,use_evalex=False)
    # app.run(debug=True,host='192.168.43.53',port=5007,use_evalex=False)
