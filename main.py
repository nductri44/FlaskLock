from flask import Flask, render_template, request, redirect, url_for, session
import MySQLdb
import MySQLdb.cursors
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

app.secret_key = '5659'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '5659'
# app.config['MYSQL_DB'] = 'pythonlogin'

conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "5659",
                           db = "pythonlogin")


cred = credentials.Certificate("home/tri/FlaskLock/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://facerecognition-49c2d-default-rtdb.asia-southeast1.firebasedatabase.app/'})


@app.route('/home')
def home():
    if 'loggedin' in session:
        postive_ref = db.reference('/face_positive')    
        data = postive_ref.get()
        return render_template('home.html', username=session['username'], places=data)
    
    return redirect(url_for('login'))

@app.route('/face_negative')
def face_negative():
    if 'loggedin' in session:
        negative_ref = db.reference('/face_negative')
        data = negative_ref.get()
        return render_template('face_negative.html', username=session['username'], places=data)
    
    return redirect(url_for('login'))

@app.route('/finger_positive')
def finger_positive():
    if 'loggedin' in session:
        postive_ref = db.reference('/finger_positive')
        data = postive_ref.get()
        return render_template('finger_positive.html', username=session['username'], places=data)
    
    return redirect(url_for('login'))

@app.route('/finger_negative')
def finger_negative():
    if 'loggedin' in session:
        negative_ref = db.reference('/finger_negative')
        data = negative_ref.get()
        return render_template('finger_negative.html', username=session['username'], places=data)
    
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('login.html', msg='') 


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
