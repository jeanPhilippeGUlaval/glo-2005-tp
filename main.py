from flask import Flask, render_template, request, session
from database import conn, cur
from listeDePrix import listeDePrix
from soumission import soumission
import pymysql
import pymysql.cursors
import random
import authentification.signup as auth
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(listeDePrix)
app.register_blueprint(soumission)


@app.route("/")
def main():
    return signin()

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/login", methods=['POST'])
def login():
    email = '"'+request.form.get('inputEmail')+'"'
    password = auth.hash_password(request.form.get('inputPassword'))
    cmd='SELECT id, password FROM users WHERE email = '+email+';'
    cur.execute(cmd)
    passeVrai = cur.fetchone()
    print(passeVrai[1])
    print(password)
    if (passeVrai!=None) and (password==passeVrai[1]):
        print("Log")
        session['id'] = passeVrai[0]
        return render_template('index.html')
    return main()



@app.route("/createAccount", methods=['POST'])
def createAccount():
    email : str
    password : str
    email = '"'+request.form.get('inputEmail')+'"'
    password = request.form.get('inputPassword')
    password = '"'+auth.hash_password(password)+'"'
    try:
        cmd='INSERT INTO users (email, password) VALUES('+email+','+password+');'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return signin()


# SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'porte' AND COLUMN_KEY = '';
if __name__ == "__main__":
    app.run()

cur.close()
conn.close()