# Import des modules nécessaires
from flask import Flask
from database import conn, cur
from listeDePrix import listeDePrix
from soumission import soumission
from authentication import authentication, signin

# Le secret KEY de l'app permet d'avoir la classe Session et garder l'ID de l'utilisateur actif.
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Enregistrement des blueprints dans l'application Flask
app.register_blueprint(listeDePrix)
app.register_blueprint(soumission)
app.register_blueprint(authentication)


# Route principale de l'application
@app.route("/")
def main():
    return signin() # Retourne la page de connexion au chargement de la page d'accueil

if __name__ == "__main__":
    app.run() # Démarrage de l'application Flask

# Fermeture de la connexion à la base de données et du curseur après l'exécution de l'application
cur.close()
conn.close()