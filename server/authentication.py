from flask import render_template, request, Blueprint, session
from config import smtp_server, sender_email, password, port
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from database import conn, cur
from random import randint
import hashlib, uuid, os


# Logique d'affaire pour l'authentification

authentication = Blueprint('authentication', __name__, template_folder='templates')

@authentication.route("/signin")
def signin(error ="", info=""):
    return render_template('signin.html', error = error, info = info)

@authentication.route("/signup")
def signup(error =""):
    return render_template('signup.html', error = error)\
    
# Logique pour valider la connexion grâce au informations entrée.
@authentication.route("/login", methods=['POST'])
def login():
    email = '"'+request.form.get('inputEmail')+'"'
    password = request.form.get('inputPassword')
    # On viens appliquer le même hashng au mot de passe afin de le comparer avec celui en mémoire.
    try:
        cmd='SELECT id, password, salt FROM users WHERE email = '+email+';'
        cur.execute(cmd)
        identifiant = cur.fetchone()
    except Exception:
        return signin("Courriel ou mot de passe invalide.")
    if identifiant == None:
        return signin("Courriel ou mot de passe invalide.")
    password = hash_password(password, identifiant[2])
    # Ici on viens chercher le mot de passe ainsi que l'identifiant de l'utilisateur afin de valider son mot de passe.
    if (identifiant!=None) and (password==identifiant[1]):
        # Si l'identification est positive, on vient mettre l'identifiant dans le dictionnaire de session.
        session['id'] = identifiant[0]
        return home()
    return signin("Courriel ou mot de passe invalide.")


# Fonction qui gère la création du compte.
# Le mot des passe est encoder à l'aide d'une fonction de hashing et est stocké dans la base de donnée.
@authentication.route("/createAccount", methods=['POST'])
def createAccount():
    email : str
    password : str
    email = '"'+request.form.get('inputEmail')+'"'
    password = request.form.get('inputPassword')
    # Ceci est le sel qui est ajouté au mot de passe pour augmenter l'encodage.
    salt = uuid.uuid4().hex
    password = '"'+ hash_password(password, salt) +'"'
    try:
        cmd='INSERT INTO users (email, password, salt) VALUES('+email+','+password+',\''+ salt+'\');'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        return signup("Erreur: Le courriel existe déjà.")
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

#Fonction qui retourne la page de mot de passe oublié.
@authentication.route("/forgotPassword")
def forgotPassword():
    return render_template('forgotPassword.html')

# Fonction qui envoi un courriel pour un oublie de mot de passe.
# On utilise le courriel et on génère un token. Par la suite, nous insérons dans une base de donnée le courriel et le token ensemble
# Ce token permet de gérer que n'importe qui ne puisse pas envoyer des demandes d'oublie de mot de passe.
# On utilise un serveur smtp.
@authentication.route("/sendForgotPassword", methods=['POST'])
def sendforgotPassword():
    email = request.form.get('inputEmail')
    if not checkIfEmailExist(email):
        return signin("","Un courriel à été envoyé avec les informations pour changer votre mot de passe")
    
    token = generateToken()
    insertTokenAndEmailInForgottenTable(email, token)
    redirectUrl = 'http://'+ os.environ.get('HOST')+ '/changePasswordPage?email=' + email +'&token='+str(token) # Création du lien de redirection pour que la personne puisse changer son mot de passe.
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        receiver_email = email    # Courriel à qui on veux changer le mot de passe.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Changez votre mot de passe"
        message = """<html>
        <body>
            <p>Vous avez fait une demande pour changer votre mot de passe?</p>
            <p>Sinon, ne cliquez pas sur ce lien et contacter l'administrateur du site.</p>
            <p><a href=\"""" + redirectUrl + """"\">Cliquez ici pour changer votre mot de passe</a></
        </body>
    </html>
""" # Message formaté en HTML pour le lien
        part2 = MIMEText(message, 'html')
        msg.attach(part2)
        server.login(sender_email, password) # Connexion à la boite de courriel d'envoi du site
        server.sendmail(sender_email, receiver_email, msg.as_string()) # Envoi du courriel.
    return signin("", "Un courriel à été envoyé avec les informations pour changer votre mot de passe")

#Cette fonction retourne la page de changement de mot de passe. Elle prend en entré le token et vérifie si celui-ci
# est toujours valide.
@authentication.route("/changePasswordPage")
def changePasswordPage():
    email = request.args.get('email')
    token = request.args.get('token', type=int)
    print(token)
    if not checkIfTokenIsValide(email, token):
        return signin("Lien expiré")
    return render_template("changePassword.html", token = token, email = email)

# Cette fonction permet de changer le mot de passe dans la base de donnée d'utilisateur.
# Elle vient aussi supprimer de la table forgotPassword l'entrée du courriel et du token.
@authentication.route("/changePassword", methods=['POST'])
def changePassword():
    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    salt = uuid.uuid4().hex
    password = '"'+ hash_password(password, salt) +'"'
    removeTokenAndEmailInForgottenTable(email)
    error = updatePassword(email, password, salt)
    if error != "":
        return signin(error)
    return signin("", "Votre mot de passe à été changé avec succès!")




# Fonction qui applique une fontion de hashage sur le mot de passe et le retourne.
def hash_password(password, salt):
   passwordSalted = password + salt
   passwordBytes = passwordSalted.encode('utf-8')
   hash_object = hashlib.sha256(passwordBytes).hexdigest()
   return hash_object

def checkIfEmailExist(email):
        cmd= 'SELECT EXISTS(SELECT ID FROM users WHERE email = \''+email+'\');'
        cur=conn.cursor()
        cur.execute(cmd)
        answer = cur.fetchone()[0]
        print(answer)
        if answer == 1:
            return True
        return False

# Fontion qui génère un token aléatoire de 8 chiffres.
def generateToken():
    return randint(10000000, 99999999)

# Fonction qui insére dans la table des mots de passe oublié le token et le courriel
def insertTokenAndEmailInForgottenTable(email, token):
    try:
        cmd = 'INSERT INTO forgottenPassword VALUES(\''+email+'\','+str(token)+');'
        print(cmd)
        cur=conn.cursor()
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)

# Fonction qui enlève le tuple dans la table des mots de passe oublié le token et le courriel
def removeTokenAndEmailInForgottenTable(email):
    try:
        cmd = 'DELETE FROM forgottenPassword WHERE email = \''+email+'\';'
        cur=conn.cursor()
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)

# Fonction qui vérifie que le token est valide dans la table des mots de passe oubliés
def checkIfTokenIsValide(email, token : int):
    try:
        storedToken : int
        cmd = 'SELECT token FROM forgottenPassword WHERE email = \''+email+'\';'
        cur=conn.cursor()
        cur.execute(cmd)
        storedToken = cur.fetchone()[0]
    except Exception:
        return False
    print(storedToken)
    if token == storedToken:
        return True
    return False

#Fonction pour mettre à jour le mot de passe.
def updatePassword(email, password, salt):
    try:
        cmd = 'UPDATE users SET password = '+password+', salt = \''+salt+'\' WHERE email = \''+email+'\';'
        cur=conn.cursor()
        cur.execute(cmd)
        conn.commit()
    except Exception:
        return "Une erreure s'est produite, veuillez contactez l'administrateur du site"
    return ""