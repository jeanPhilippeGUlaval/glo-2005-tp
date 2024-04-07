from flask import render_template, request, Blueprint
from database import *
from listeDePrix import getHeaders
from authentication import signin


soumission = Blueprint('soumission', __name__, template_folder='templates')

# Fonction qui affiche la page principal des soumissions d'un utilisateur.
@soumission.route("/soumission", methods=["GET"])
def displaySoumissionID(soumissionID =""):
    if session['id'] == None:
        return signin()
    if soumissionID == "":
        soumissionID = request.args.get('id')
    if soumissionID == "" or soumissionID == None:
        ListOfSoumissions = getSoumissionList()
        headersData = getHeaders("soumission")
        tableData = []
        soumissionID = "Soumission"
    else:
        ListOfSoumissions, tableData, headersData, soumissionID = getData(soumissionID)
    return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, headers=headersData, soumissionID=soumissionID, total=getTotal(soumissionID))

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
    ListOfSoumissions = getSoumissionList()
    headersData = getHeaders("soumission")
    tableData = []
    soumissionID = "Soumission"
    return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, headers=headersData, soumissionID=soumissionID)

# Fonction qui retourne les informations d'une soumission spécifique.
def getData(soumissionID):
    ListOfSoumissions = getSoumissionList()
    headersData = getHeaders("soumission")
    cmd = 'SELECT UPPER(TAG), ID, Prix , catégorie,sQuantite, sTotal FROM soumission_asso_produits d INNER JOIN produits p ON d.ProductID = p.ID AND d.sID = \'' + soumissionID + '\' AND d.userID = ' + str(session["id"]) + ';'
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return ListOfSoumissions, tableData, headersData, soumissionID

# Fonction qui retourne la liste des soumissions de l'utilisateur actif.
def getSoumissionList():
    try:
        cmd = 'SELECT * FROM soumission_ids WHERE userID = ' + str(session["id"]) + ';'
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(e)
    return tableData

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