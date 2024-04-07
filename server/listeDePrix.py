from flask import render_template, request, Blueprint, session
from database import conn, cur, TABLE_PRODUIT
from authentication import signin
import re


listeDePrix = Blueprint('listeDePrix', __name__, template_folder='templates')

# Cette fonction permet d'être générique pour tout les affichages de tables de produits.
def display(table, title):
    if table in TABLE_PRODUIT:
        headersData = getHeaders(table)
        soumissions = getSoumissions(session["id"])
        cmd = getCmdWithHeaders(table, "p.Catégorie, t.Hauteur, t.Largeur")
        try:
            cur=conn.cursor()
            cur.execute(cmd)
            tableData = cur.fetchall()
            return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions)
        except Exception as e:
            print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId="porte", soumissions=soumissions)

@listeDePrix.route("/listeDePrix/porte", methods=['GET'])
def displayListeDePrixForPorte():
    if session['id'] == None:
        return signin()
    return display("porte", "Porte de Garage")

@listeDePrix.route("/listeDePrix/panneaux", methods=['GET'])
def displayListeDePrixForPanneaux():
    if session['id'] == None:
        return signin()
    return display("panneaux", "Panneaux")


@listeDePrix.route("/listeDePrix/ferronnerie", methods=['GET'])
def displayListeDePrixForFerronnerie():
    if session['id'] == None:
        return signin()
    return display("ferronnerie", "Ferronnerie")    

@listeDePrix.route("/listeDePrix/search", methods=['GET'])
def index():
    if session['id'] == None:
        return signin()
    search_term = request.args.get('search', '')
    search_term = re.sub(r'\W+', '', search_term)

    product = request.args.get('product', '')
    if product not in TABLE_PRODUIT:
        return display("porte", "Porte de Garage")
    
    title = request.args.get('title')
    headersData = getHeaders(product)
    soumissions = getSoumissions(session["id"])
    
    if search_term:
        cmd = getCmdWithHeadersWithSearch(product, search_term)
    else:
        cmd = getCmdWithHeaders(product, "p.Catégorie, t.Hauteur, t.Largeur")
    cur=conn.cursor()
    cur.execute(cmd)
    tableData = cur.fetchall()
    cur.close()
    if tableData == None:
        return display("porte", "Porte de Garage")
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=product, soumissions=soumissions)


@listeDePrix.route("/listeDePrix/orderBy", methods=['GET'])
def displayListeDePrixForOrderBy():
    if session['id'] == None:
        return signin()
    orderBy = request.form.get('orderBy')
    table = request.form.get('table')
    if table not in TABLE_PRODUIT:
        return display("porte", "Porte de Garage")
    title = request.form.get('title')
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(table, orderBy)
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data = tableData, tableId=table, soumissions=soumissions)

@listeDePrix.route("/product/addToSoumission", methods=['POST'])
def addItemToSoumission():
    if session['id'] == None:
        return signin()
    productID = request.form.get('productID', type=int)
    getQty = ''+str(productID) +'-qty'
    print(getQty)
    qty = request.form.get(getQty)
    print(qty)
    soumissionID = request.form.get('soumissionID')
    try:
        cmd = 'CALL AjouterSoumission('+str(productID)+', '+str(qty)+', \''+soumissionID+'\');'
        print(cmd)
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return "Ok"


def getHeaders(table):
    try:
        cmd='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \''+table+'\' ORDER BY ORDINAL_POSITION;'
        cur=conn.cursor()
        cur.execute(cmd)
        headersData = [row[0] for row in cur.fetchall()]
        return headersData
    except Exception as e:
        print(e)
    return

def getCmdWithHeaders(table):
    return 'SELECT p.Catégorie, t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie prix FROM produits) p;'

def getCmdWithHeaders(table, orderBy):
    return 'SELECT p.Catégorie,t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p ORDER BY '+ orderBy + ';'

def getCmdWithHeadersWithSearch(table, search_term, orderBy = ""):
    if orderBy == "":
        return 'SELECT p.Catégorie, t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p WHERE p.Catégorie LIKE \'%' + search_term + '%\''
    else:
        return 'SELECT p.Catégorie,t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p WHERE p.Catégorie LIKE \'%' + search_term + '%\' ORDER BY '+ orderBy + ';'

# Cette fonction permet de 
def getSoumissions(userID):
    try:
        cmd= 'SELECT ID FROM soumission_ids WHERE userID = '+str(userID)+';'
        cur=conn.cursor()
        cur.execute(cmd)
        soumissions = [row[0] for row in cur.fetchall()]
        return soumissions
    except Exception as e:
        print(e)
    return

