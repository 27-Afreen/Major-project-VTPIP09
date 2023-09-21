from flask import Flask, render_template, request, session, flash
from werkzeug.utils import secure_filename
import cv2 
import os
import math, random

app = Flask(__name__)

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="vtpip09_2022"
)

app.secret_key = 'your secret key'

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/doctor')
def doctor():
    return render_template('doctor.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/alogin', methods = ['POST', 'GET'])
def alogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'lab' and pwd == 'lab':
            return render_template('ahome.html')
        else:
            return render_template('admin.html')

@app.route('/ulogin', methods = ['POST', 'GET'])
def ulogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            return render_template('uhome.html', result = account[0])
        else:
            flash("Please Enter Valid Details...")
            return render_template('user.html')

@app.route('/dlogin', methods = ['POST', 'GET'])
def dlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            session['man'] = account[4]
            return render_template('dhome.html', result = account[0])
        else:
            return render_template('doctor.html')

@app.route('/lhome')
def lhome():
    return render_template('ahome.html')

@app.route('/uregister')
def uregister():
    return render_template('ureg.html')

@app.route('/dregister')
def dregister():
    return render_template('dreg.html')

@app.route('/dreg', methods = ['POST', 'GET'])
def dreg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        dep = request.form['dep']
        var = (name, uid, pwd, mob, dep)
        cursor = mydb.cursor()
        cursor.execute('insert into doctor values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Doctor Registered Successfuly") 
            return render_template('doctor.html')
        else:
            flash("Invalid Details, Doctor not Registered")
            return render_template('dreg.html')

@app.route('/ureg', methods = ['POST', 'GET'])
def ureg():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        pwd = request.form['pwd']
        mob = request.form['mob']
        loc = request.form['loc']
        var = (name, uid, pwd, mob, loc)
        cursor = mydb.cursor()
        cursor.execute('insert into user values (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("User Registered Successfuly") 
            return render_template('user.html')
        else:
            flash("Invalid Details, User not Registered")
            return render_template('ureg.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

@app.route('/duser')
def duser():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'pending'")
    account = cursor.fetchall()
    return render_template('duser.html', result = account)

@app.route('/dreport')
def dreport():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'completed'")
    account = cursor.fetchone()
    return render_template("dreport.html", result = account)

@app.route('/udoc')
def udoc():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor')
    account = cursor.fetchall()
    return render_template("udoc.html", result = account)

@app.route('/ureport')
def ureport():
    uid = session['uid']
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE email = '"+uid+"' and status= 'completed'")
    account = cursor.fetchone()
    return render_template("ureport.html", result = account)

@app.route('/usend', methods = ['POST', 'GET'])
def usend():
    if request.method == 'POST':
        name = session['name']
        uid = session['uid']
        sym = request.form['sym']
        did = request.form['did']
        var = (name, uid, sym, did)
        cursor = mydb.cursor()
        cursor.execute('insert into userdet values (0, %s, %s, %s, %s, "pending")', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("User Registered Successfuly") 
            return render_template('uhome.html', result = name)
        else:
            flash("Invalid Details, User not Registered")
            cursor.execute('SELECT * FROM doctor')
            account = cursor.fetchall()
            return render_template("udoc.html", result = account)

@app.route('/dsend/<string:id>')
def dsend(id):
    cursor = mydb.cursor()
    cursor.execute("update userdet set status ='process' WHERE Id = "+ id)
    mydb.commit()
    if cursor.rowcount == 1:
        return render_template('dhome.html', result = session['name'])
    else:
        uid = session['uid']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM userdet WHERE DocId = '"+uid+"' and status= 'pending'")
        account = cursor.fetchall()
        return render_template('duser.html', result = account)
    
@app.route('/sreport')
def sreport():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE status= 'process'")
    account = cursor.fetchall()
    return render_template('sreport.html', result = account)

@app.route('/ssend/<string:id>')
def ssend(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM userdet WHERE id="+id)
    account = cursor.fetchone()
    return render_template('ssend.html', result = account)
    
@app.route('/send', methods = ['POST', 'GET'])
def send():
    if request.method == 'POST':
        cid = request.form['id']
        name = request.form['name']
        uid = request.form['uid']
        did = request.form['did']
        f = request.files['file']
        fname = "C:/MajorProject/VTPIP09_2022/static/"+f.filename
        f.save(secure_filename(f.filename))
        img = cv2.imread(f.filename)
        cv2.imwrite(fname, img) 
        key = token()
        var = (cid, name, uid, did, f.filename, key)
        cursor = mydb.cursor()
        cursor.execute('insert into sreport values (%s, %s, %s, %s, %s, %s)', var)
        mydb.commit()
        os.remove(f.filename)
        if cursor.rowcount == 1:
            cursor.execute("update userdet set status ='completed' WHERE Id = "+ cid)
            mydb.commit()
            return render_template('ahome.html')
        else:
            cursor.execute("SELECT * FROM userdet WHERE status= 'process'")
            account = cursor.fetchall()
            return render_template('sreport.html', result = account)

@app.route('/drep/<string:id>')
def drep(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+id)
    account = cursor.fetchone()
    print(account)
    session['id'] = id
    session['fname'] = account[0]
    return render_template('drep.html')

@app.route('/drequest')
def drequest():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT key1 FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('drequest.html', result = account)

@app.route('/display')
def display():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('display.html', result = account)

@app.route('/urep/<string:id>')
def urep(id):
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+id)
    account = cursor.fetchone()
    print(account)
    session['id'] = id
    session['fname'] = account[0]
    return render_template('urep.html')

@app.route('/urequest')
def urequest():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT key1 FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('urequest.html', result = account)

@app.route('/udisplay')
def udisplay():
    cid = session['id']
    cursor = mydb.cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id= "+cid)
    account = cursor.fetchone()
    return render_template('udisplay.html', result = account)

def token():
    st = "abcdefijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(st)
    OTP = ""
    for i in range(10) :
        OTP += st[math.floor(random.random() * length)]
    return OTP

if __name__ == '__main__':
   app.run()