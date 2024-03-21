from flask import Flask, render_template, request
import pymysql
import pymysql.cursors
import random
import authentification.signup as auth
import os
from dotenv import load_dotenv

load_dotenv(override=True)
app = Flask(__name__)
conn = pymysql.connect(
        host= os.environ.get("HOST"),
        user= os.environ.get("USER"),
        password= os.environ.get("PASSWORD"),
        db= os.environ.get("DATABASE") )
cur = conn.cursor()

@app.route("/")
def main():
    return signin()

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/login", methods=['POST'])
def login():
    email = '"'+request.form.get('inputEmail')+'"'
    password = auth.hash_password(request.form.get('inputPassword'))
    cmd='SELECT password FROM users WHERE email = '+email+';'
    cur.execute(cmd)
    passeVrai = cur.fetchone()
    if (passeVrai!=None) and (password==passeVrai[0]):
        return render_template('index.html')
    return main()



@app.route("/createAccount", methods=['POST'])
def createAccount():
    email : str
    password : str
    email = '"'+request.form.get('inputEmail')+'"'
    password = request.form.get('inputPassword')
    password = '"'+auth.hash_password(password)+'"'
    id = random.randint(0, 2147483647)
    print('INSERT INTO users VALUES('+str(id)+', '+email+','+password+');')
    try:
        cmd='INSERT INTO users VALUES('+str(id)+', '+email+','+password+');'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return signin()
    
if __name__ == "__main__":
    app.run()

cur.close()
conn.close()