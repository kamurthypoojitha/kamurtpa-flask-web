from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sqlite3
import os

app = Flask(__name__)

DATABASE = '/home/ubuntu/flaskapp/users.db'
UPLOAD_FOLDER = '/home/ubuntu/flaskapp/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    address = request.form['address']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
              (username, password, firstname, lastname, email, address))
    conn.commit()
    conn.close()

    return redirect(url_for('profile', username=username))


@app.route('/profile/<username>')
def profile(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    word_count = None
    filepath = os.path.join(UPLOAD_FOLDER, 'Limerick.txt')

    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            words = f.read().split()
            word_count = len(words)

    return render_template('profile.html', user=user, word_count=word_count)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/relogin', methods=['POST'])
def relogin():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('profile', username=username))
    else:
        return "Invalid username or password"


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, 'Limerick.txt'))
    return redirect(request.referrer)


@app.route('/download')
def download():
    return send_from_directory(UPLOAD_FOLDER, 'Limerick.txt', as_attachment=True)
