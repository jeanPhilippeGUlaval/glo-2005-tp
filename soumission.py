from flask import Flask, render_template, request, Blueprint
from database import conn, cur
from listeDePrix import getHeaders


soumission = Blueprint('soumission', __name__, template_folder='templates')

@soumission.route("/soumission", methods=["GET"])
def displaySoumissionID():
    soumissionID : str
    soumissionID = request.args.get('id')
    ListOfSoumissions, tableData, headersData, soumissionID = getData(soumissionID)
    return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, headers=headersData, soumissionID=soumissionID)

@soumission.route("/soumission/addSoumission", methods=['POST'])
def addSoumission():
    newSoumissionID = request.form.get('inputSoumissionID')
    if newSoumissionID.find(" ") != -1:
        ListOfSoumissions, tableData, headersData, soumissionID = getData(soumissionID)
        return render_template("soumission.html", lsSoumission=ListOfSoumissions, data = tableData, headers=headersData, soumissionID=soumissionID, error="Il ne peux pas avoir d'espace dans l'identifiant")
    else:
        try:
            cmd = 'INSERT INTO soumission_ids VALUES (\''+ newSoumissionID +'\');'
            cur=conn.cursor()
            cur.execute(cmd)
        except Exception as e:
            print(e)

def getData(soumissionID):
    ListOfSoumissions = getSoumissionList()
    headersData = getHeaders("soumission")
    if soumissionID == None:
        cmd = 'SELECT * FROM soumission;'
        soumissionID = "Toutes les Soumissions"
    else:
        cmd = 'SELECT * FROM soumission WHERE ID = \''+soumissionID + '\';'
    try:
        print(cmd)
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return ListOfSoumissions, tableData, headersData, soumissionID

def getSoumissionList():
    try:
        cmd = "SELECT * FROM soumission_ids;"
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(e)
    return tableData

