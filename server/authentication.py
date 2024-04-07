from flask import render_template, request, Blueprint, session
from database import conn, cur
import hashlib


# Logique d'affaire pour l'authentification

authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route("/signin")
def signin():
    return render_template('signin.html', error="")

@authentication.route("/signup")
def signup():
    return render_template('signup.html')\
    
# Logique pour valider la connexion grâce au informations entrée.
@authentication.route("/login", methods=['POST'])
def login():
    email = '"'+request.form.get('inputEmail')+'"'
    # On viens appliquer le même hashng au mot de passe afin de le comparer avec celui en mémoire.
    password = hash_password(request.form.get('inputPassword'))
    # Ici on viens chercher le mot de passe ainsi que l'identifiant de l'utilisateur afin de valider son mot de passe.
    cmd='SELECT id, password FROM users WHERE email = '+email+';'
    cur.execute(cmd)
    identifiant = cur.fetchone()
    if (identifiant!=None) and (password==identifiant[1]):
        # Si l'identification est positive, on vient mettre l'identifiant dans le dictionnaire de session.
        session['id'] = identifiant[0]
        return home()
    return render_template('signin.html', error="Courriel ou mot de passe invalide.")


# Fonction qui gère la création du compte.
# Le mot des passe est encoder à l'aide d'une fonction de hashing et est stocké dans la base de donnée.
@authentication.route("/createAccount", methods=['POST'])
def createAccount():
    email : str
    password : str
    email = '"'+request.form.get('inputEmail')+'"'
    password = request.form.get('inputPassword')
    password = '"'+ hash_password(password) +'"'
    try:
        cmd='INSERT INTO users (email, password) VALUES('+email+','+password+');'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return signin()

# Prendre note que tant et aussi longtemps que l'utilisateur n'est pas connecter, il n'a pas accès
# à l'application.
@authentication.route("/home")
def home():
    if session['id'] == None:
        return signin()
    return render_template('index.html')

# Fonction de logout, elle efface le ID du dictionnaire session.
@authentication.route("/logout")
def logout():
    session['id'] = None
    return signin()

# Fonction qui applique une fontion de hashage sur le mot de passe et le retourne.
def hash_password(password):
   password_bytes = password.encode('utf-8')
   hash_object = hashlib.sha256(password_bytes)
   return hash_object.hexdigest()