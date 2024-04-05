from flask import Flask, render_template, request, session
from database import conn, cur
from listeDePrix import listeDePrix
from soumission import soumission
from authentication import authentication, signin
import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.register_blueprint(listeDePrix)
app.register_blueprint(soumission)
app.register_blueprint(authentication)


@app.route("/")
def main():
    return signin()

if __name__ == "__main__":
    app.run()

cur.close()
conn.close()