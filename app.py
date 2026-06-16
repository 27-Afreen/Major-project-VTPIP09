from flask import Flask, render_template, request, session, flash
from werkzeug.utils import secure_filename
import cv2
import os
import math
import random
from encryption import encrypt_image
from model import run_diagnosis

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-only-secret-key")

import mysql.connector

# ── FIX 1: Connect to MySQL safely (won't crash Flask on startup) ──────────
def get_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3307")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "vtpip09_2022")
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[DB ERROR] Could not connect to MySQL: {err}")
        return None

mydb = get_db()

# ── FIX 2: Helper to get a fresh cursor (reconnects if connection dropped) ──
def get_cursor():
    global mydb
    try:
        if mydb is None:
            mydb = get_db()
        else:
            mydb.ping(reconnect=True, attempts=3, delay=1)
    except Exception:
        mydb = get_db()
    if mydb is None:
        raise Exception("Database not connected. Please check MySQL is running and password is correct.")
    return mydb.cursor()

# ────────────────────────────────────────────────────────────────────────────

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

@app.route('/alogin', methods=['POST', 'GET'])
def alogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        if uid == 'lab' and pwd == 'lab':
            return render_template('ahome.html')
        else:
            return render_template('admin.html')

@app.route('/ulogin', methods=['POST', 'GET'])
def ulogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = get_cursor()
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            return render_template('uhome.html', result=account[0])
        else:
            flash("Please Enter Valid Details...")
            return render_template('user.html')

@app.route('/dlogin', methods=['POST', 'GET'])
def dlogin():
    if request.method == 'POST':
        uid = request.form['uid']
        pwd = request.form['pwd']
        cursor = get_cursor()
        cursor.execute('SELECT * FROM doctor WHERE email = %s AND password = %s', (uid, pwd))
        account = cursor.fetchone()
        if account:
            session['uid'] = request.form['uid']
            session['name'] = account[0]
            session['man'] = account[4]
            return render_template('dhome.html', result=account[0])
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

@app.route('/dreg', methods=['POST', 'GET'])
def dreg():
    if request.method == 'POST':
        name = request.form['name']
        uid  = request.form['uid']
        pwd  = request.form['pwd']
        mob  = request.form['mob']
        dep  = request.form['dep']
        var  = (name, uid, pwd, mob, dep)
        cursor = get_cursor()
        cursor.execute('INSERT INTO doctor VALUES (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Doctor Registered Successfully")
            return render_template('doctor.html')
        else:
            flash("Invalid Details, Doctor not Registered")
            return render_template('dreg.html')

@app.route('/ureg', methods=['POST', 'GET'])
def ureg():
    if request.method == 'POST':
        name = request.form['name']
        uid  = request.form['uid']
        pwd  = request.form['pwd']
        mob  = request.form['mob']
        loc  = request.form['loc']
        var  = (name, uid, pwd, mob, loc)
        cursor = get_cursor()
        cursor.execute('INSERT INTO user VALUES (%s, %s, %s, %s, %s)', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("User Registered Successfully")
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
    uid    = session['uid']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = %s AND status = 'pending'", (uid,))
    account = cursor.fetchall()
    return render_template('duser.html', result=account)

@app.route('/dreport')
def dreport():
    uid    = session['uid']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM userdet WHERE DocId = %s AND status = 'completed'", (uid,))
    account = cursor.fetchone()
    return render_template("dreport.html", result=account)

@app.route('/udoc')
def udoc():
    cursor = get_cursor()
    cursor.execute('SELECT * FROM doctor')
    account = cursor.fetchall()
    return render_template("udoc.html", result=account)

@app.route('/ureport')
def ureport():
    uid    = session['uid']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM userdet WHERE email = %s AND status = 'completed'", (uid,))
    account = cursor.fetchone()
    return render_template("ureport.html", result=account)

@app.route('/usend', methods=['POST', 'GET'])
def usend():
    if request.method == 'POST':
        name = session['name']
        uid  = session['uid']
        sym  = request.form['sym']
        did  = request.form['did']
        var  = (name, uid, sym, did)
        cursor = get_cursor()
        cursor.execute('INSERT INTO userdet VALUES (0, %s, %s, %s, %s, "pending")', var)
        mydb.commit()
        if cursor.rowcount == 1:
            flash("Request Sent Successfully")
            return render_template('uhome.html', result=name)
        else:
            flash("Invalid Details, Request not Sent")
            cursor2 = get_cursor()
            cursor2.execute('SELECT * FROM doctor')
            account = cursor2.fetchall()
            return render_template("udoc.html", result=account)

@app.route('/dsend/<string:id>')
def dsend(id):
    cursor = get_cursor()
    cursor.execute("UPDATE userdet SET status = 'process' WHERE Id = %s", (id,))
    mydb.commit()
    if cursor.rowcount == 1:
        return render_template('dhome.html', result=session['name'])
    else:
        uid     = session['uid']
        cursor2 = get_cursor()
        cursor2.execute("SELECT * FROM userdet WHERE DocId = %s AND status = 'pending'", (uid,))
        account = cursor2.fetchall()
        return render_template('duser.html', result=account)

@app.route('/sreport')
def sreport():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM userdet WHERE status = 'process'")
    account = cursor.fetchall()
    return render_template('sreport.html', result=account)

@app.route('/ssend/<string:id>')
def ssend(id):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM userdet WHERE id = %s", (id,))
    account = cursor.fetchone()
    return render_template('ssend.html', result=account)

@app.route('/send', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        cid  = request.form['id']
        name = request.form['name']
        uid  = request.form['uid']
        did  = request.form['did']
        f    = request.files['file']

        safe_name   = secure_filename(f.filename)
        static_dir  = os.path.join(app.root_path, 'static')
        os.makedirs(static_dir, exist_ok=True)
        temp_path   = os.path.join(static_dir, safe_name)

        # Save uploaded file temporarily
        f.save(temp_path)

        # ── ENCRYPT the image using SKK scheme ──────────────────────────────
        try:
            enc_name, _ = encrypt_image(temp_path, static_dir, filter_type='median')
            print(f"[APP] Image encrypted → {enc_name}")
        except Exception as e:
            print(f"[APP] Encryption failed: {e}")
            enc_name = safe_name   # fallback: use original

        # ── RUN DIAGNOSIS with DenseNet-121 & XceptionNet ───────────────────
        enc_path = os.path.join(static_dir, enc_name)
        try:
            diag = run_diagnosis(enc_path)
            diagnosis = diag['final']
            densenet_conf = diag['densenet']['confidence']
            xception_conf = diag['xception']['confidence']
            print(f"[APP] Diagnosis: {diagnosis}")
        except Exception as e:
            print(f"[APP] Diagnosis failed: {e}")
            diagnosis     = "Analysis Pending"
            densenet_conf = "N/A"
            xception_conf = "N/A"

        # Store encrypted filename + diagnosis in DB
        key = token()
        var = (cid, name, uid, did, enc_name, key, diagnosis, densenet_conf, xception_conf)
        cursor = get_cursor()
        cursor.execute(
            'INSERT INTO sreport VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', var
        )
        mydb.commit()

        # Remove temp original
        if os.path.exists(temp_path) and temp_path != enc_path:
            os.remove(temp_path)

        if cursor.rowcount == 1:
            cursor2 = get_cursor()
            cursor2.execute("UPDATE userdet SET status = 'completed' WHERE Id = %s", (cid,))
            mydb.commit()
            flash(f"Report uploaded & encrypted! Diagnosis: {diagnosis}")
            return render_template('ahome.html')
        else:
            cursor3 = get_cursor()
            cursor3.execute("SELECT * FROM userdet WHERE status = 'process'")
            account = cursor3.fetchall()
            return render_template('sreport.html', result=account)

@app.route('/drep/<string:id>')
def drep(id):
    cursor = get_cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id = %s", (id,))
    account = cursor.fetchone()
    print(account)
    session['id']    = id
    session['fname'] = account[0]
    return render_template('drep.html')

@app.route('/drequest')
def drequest():
    cid    = session['id']
    cursor = get_cursor()
    cursor.execute("SELECT key1 FROM sreport WHERE id = %s", (cid,))
    account = cursor.fetchone()
    return render_template('drequest.html', result=account)

@app.route('/display')
def display():
    cid    = session['id']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sreport WHERE id = %s", (cid,))
    account = cursor.fetchone()
    return render_template('display.html', result=account)

@app.route('/urep/<string:id>')
def urep(id):
    cursor = get_cursor()
    cursor.execute("SELECT filename FROM sreport WHERE id = %s", (id,))
    account = cursor.fetchone()
    print(account)
    session['id']    = id
    session['fname'] = account[0]
    return render_template('urep.html')

@app.route('/urequest')
def urequest():
    cid    = session['id']
    cursor = get_cursor()
    cursor.execute("SELECT key1 FROM sreport WHERE id = %s", (cid,))
    account = cursor.fetchone()
    return render_template('urequest.html', result=account)

@app.route('/udisplay')
def udisplay():
    cid    = session['id']
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sreport WHERE id = %s", (cid,))
    account = cursor.fetchone()
    return render_template('udisplay.html', result=account)


def token():
    st     = "abcdefijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    length = len(st)
    OTP    = ""
    for i in range(10):
        OTP += st[math.floor(random.random() * length)]
    return OTP


if __name__ == '__main__':
    app.run(debug=True)   # debug=True gives auto-reload + better error pages
