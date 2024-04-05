from flask import Flask, render_template, request, Blueprint, session
from database import conn, cur
import pymysql.cursors
import authentification.signup as auth
from dotenv import load_dotenv


authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route("/signin")
def signin():
    return render_template('signin.html', error="")

@authentication.route("/signup")
def signup():
    return render_template('signup.html')\
    

@authentication.route("/login", methods=['POST'])
def login():
    email = '"'+request.form.get('inputEmail')+'"'
    password = auth.hash_password(request.form.get('inputPassword'))
    cmd='SELECT id, password FROM users WHERE email = '+email+';'
    cur.execute(cmd)
    identifiant = cur.fetchone()
    if (identifiant!=None) and (password==identifiant[1]):
        session['id'] = identifiant[0]
        return home()
    return render_template('signin.html', error="Courriel ou mot de passe invalide.")



@authentication.route("/createAccount", methods=['POST'])
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


@authentication.route("/home")
def home():
    if session['id'] == None:
        return signin()
    return render_template('index.html')

@authentication.route("/logout")
def logout():
    session['id'] = None
    return signin()