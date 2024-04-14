from flask import render_template, request, Blueprint
from database import *
from authentication import signin
from config import smtp_server, sender_email, password, port
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from common import getHeaders, getAllSoumissionList
import smtplib, ssl, csv


soumission = Blueprint('soumission', __name__, template_folder='templates')

# Fonction qui affiche la page principal des soumissions d'un utilisateur.
@soumission.route("/soumission", methods=["GET"])
def displaySoumissionID(soumissionID ="", erreur = ""):
    envoye = 0
    date = 0
    if session['id'] == None:
        return signin()
    if soumissionID == "":
        soumissionID = request.args.get('id')
    if soumissionID == "" or soumissionID == None:
        ListOfSoumissions = getAllSoumissionList()
        headersData = getHeaders("soumission")
        tableData = []
        soumissionID = "Soumission"
    else:
        ListOfSoumissions, tableData, headersData, soumissionID = getData(soumissionID)
        envoye, date = getSoumissionMetadata(soumissionID)
    return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, 
                           headers=headersData, soumissionID=soumissionID, total=getTotal(soumissionID), error = erreur, 
                           envoye = envoye, date = date)

# Fonction qui vient créer une nouvelle soumission.
# IN: soumissionID
# Afin de limiter les risques de scripts malicieux, si l'utilisateurs à mis des espaces dans son nom de soumission
# on retourne une erreur. Sinon, on ajoute la soumission dans la liste de soumissions.
@soumission.route("/soumission/addSoumission", methods=['POST'])
def addSoumission():
    if session['id'] == None:
        return signin()
    newSoumissionID = request.form.get('inputSoumissionID')
    if newSoumissionID.find(" ") != -1:
        ListOfSoumissions, tableData, headersData, soumissionID = getData("")
        return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, headers=headersData, soumissionID=soumissionID, error="Il ne peux pas avoir d'espace dans l'identifiant")
    else:
        try:
            userID = get_session_user()
            cmd = 'INSERT INTO soumission_ids (ID, userID) VALUES (\''+ newSoumissionID +'\', '+str(userID)+' );'
            cur.execute(cmd)
            conn.commit()
        except Exception as e:
            print(e)
    return displaySoumissionID(newSoumissionID)

# Fonction qui viens supprimer une soumission d'un utilisateur.
@soumission.route("/soumission/supprimerSoumission", methods=['GET'])
def deleteSoumission():
    if session['id'] == None:
        return signin()
    SoumissionID = request.args.get('id')
    try:
        cmd = 'DELETE FROM soumission_ids WHERE ID = \''+ SoumissionID +'\';'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return displaySoumissionID()

# Fonction qui envoi les courriels de confirmation avec la soumission.
@soumission.route("/soumission/envoyerSoumission", methods=['GET'])
def envoyeSoumission():
    SoumissionID = request.args.get('id')
    email = getEmailofActiveUser()
    # Si jamais, une erreur s'est produite et que l'utilisateur n'était pas valide, il ne peux pas envoyé de courriel
    if email == "":
        return displaySoumissionID()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        receiver_email = getEmailofActiveUser()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Confirmation de la soumission: "+ SoumissionID

        formatTableForEmail(SoumissionID)

        part2 = MIMEBase('application', "octet-stream") #Création d'un stream d'octet pour envoyé le fichier CSV
        part2.set_payload(open("/tmp/soumiTemp.csv", "rb").read())  #Ouverture du fichier pour lecture, on le met en payload dans le courriel
        encode_base64(part2) # Encode le payload
        part2.add_header('Content-Disposition', 'attachment; filename="soumission_'+SoumissionID+'.csv"') #Ajoute le fichier en header pour qu'il soit disponible.
        
        msg.attach(MIMEText("Confirmation de votre soumission envoyé", 'text'))
        msg.attach(part2)

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        erreur = setEnvoyeToTrue(SoumissionID) # Ici on vient marqué dans la base de donnée que la soumission à été envoyé afin qu'elle ne soit pas réenvoyé inutilement.
        if erreur != "":
            return displaySoumissionID("",erreur)
    return displaySoumissionID()


# Fonction pour enlever un item de ka soumission.
@soumission.route("/soumission/removeItem", methods=['POST'])
def deleteItemFromSoumission():
    if session['id'] == None:
        return signin()
    SoumissionID = request.form.get('soumissionID')
    productID = request.form.get('productID', type=int)
    try:
        cmd = 'DELETE FROM soumission_asso_produits WHERE sID = \''+ SoumissionID +'\' AND ProductID = '+str(productID)+';'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        displaySoumissionID(SoumissionID, "Une erreure s'est produite, veuillez rafraichir la page et réessayer.")
    return displaySoumissionID(SoumissionID)

# Fonction qui retourne les informations d'une soumission spécifique.
def getData(soumissionID):
    ListOfSoumissions = getAllSoumissionList()
    headersData = getHeaders("soumission")
    cmd = 'SELECT UPPER(TAG), ID, Prix , catégorie,sQuantite, sTotal FROM soumission_asso_produits d INNER JOIN produits p ON d.ProductID = p.ID AND d.sID = \'' + soumissionID + '\';'
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return ListOfSoumissions, tableData, headersData, soumissionID

# Retourne les information lié à la soumission (s'il est déjà envoyé et la date de création)
def getSoumissionMetadata(soumissionID):
    try:
        cmd = 'SELECT envoye, dateSoumission FROM soumission_ids WHERE ID = \''+soumissionID+'\';'
        cur=conn.cursor()
        cur.execute(cmd)
        metadata = cur.fetchone()
    except Exception as e:
        print(e)
    if metadata != None:
        return metadata[0], metadata[1]
    return 0, 0


# Fonction qui calcul le total de la soumission et retourne en format FLOAT. 
# Exception, si le total est nul, on retourne 0.
def getTotal(sId):
    try:
        cmd = "SELECT SUM(t.subTotal) FROM (SELECT SUM(sTotal) AS subTotal FROM soumission_asso_produits WHERE sID = \'" + sId + "\') t;"
        cur=conn.cursor()
        cur.execute(cmd)
        total = cur.fetchone()[0]
        if total == None:
            total = 0
    except Exception as e:
        print(e)
    return float(total)

def getEmailofActiveUser():
    id = session['id']
    try:
        cmd = 'SELECT email FROM users WHERE ID = '+str(id)+';'
        cur=conn.cursor()
        cur.execute(cmd)
        email = cur.fetchone()[0]
    except Exception:
        return ""
    return email

# Foncion qui vient prendre la table de donnée avec la bonne soumission et la met dans un fichier
# csv temporaire. Ce fichier sera ensuite lu afin d'être envoyé par courriel.
def formatTableForEmail(soumissionID):
    _, tableData, _ ,_ = getData(soumissionID)
    fp = open('/tmp/soumiTemp.csv', 'w')    # You pick a name, it's temporary
    attach_file = csv.writer(fp)
    attach_file.writerows(tableData)
    fp.close()
    return attach_file

# Fonction qui vient mettre à jour la table des soumissions pour inscrire si celle-ci est à jour.
def setEnvoyeToTrue(soumissionID):
    try:
        cmd = 'UPDATE soumission_ids SET envoye = 1 WHERE ID = \''+soumissionID+'\';'
        cur=conn.cursor()
        cur.execute(cmd)
        conn.commit()
    except Exception:
        return "Erreur: Veuillez réessayer plus tard."
    return ""