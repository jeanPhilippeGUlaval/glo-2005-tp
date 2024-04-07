from flask import Flask
from database import conn, cur
from listeDePrix import listeDePrix
from soumission import soumission
from authentication import authentication, signin

# Le secret KEY de l'app permet d'avoir la classe Session et garder l'ID de l'utilisateur actif.
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