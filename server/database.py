from flask import session
import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

# Cette constante permet d'ajouter une couche de sécurité car elle empêche un utilisateur d'accèder
# à une table qui n'est pas dans les tables de produits grâce à de l'injection
TABLE_PRODUIT = ["porte","panneaux","ferronnerie"]


load_dotenv(override=True)
# On vient gérer la connexion à la base de donnée
conn = pymysql.connect(
        host= os.environ.get("BDHOST"),
        user= os.environ.get("USER"),
        password= os.environ.get("PASSWORD"),
        db= os.environ.get("DATABASE") )
cur = conn.cursor()

# On retourne l'utilisateur qui est actif dans la session.
def get_session_user():
    if 'id' not in session:
        return None
    # fetch the user from database somehow
    return session['id']
