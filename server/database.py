from flask import session
import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv(override=True)
# On vient gérer la connexion à la base de donnée
conn = pymysql.connect(
        host= os.environ.get("HOST"),
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