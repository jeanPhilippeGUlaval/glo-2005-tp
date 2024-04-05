from flask import Flask, render_template, request, Blueprint, session
from database import conn, cur
import pymysql.cursors
from authentication import signin


listeDePrix = Blueprint('listeDePrix', __name__, template_folder='templates')


@listeDePrix.route("/listeDePrix/porte", methods=['GET'])
def displayListeDePrixFor():
    if session['id'] == None:
        return signin()
    table = "porte"
    title = "Porte de Garage"
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(headersData, table, "Catégorie, Hauteur, Largeur")
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
        return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions)
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId=table, soumissions=soumissions)


@listeDePrix.route("/listeDePrix/panneaux", methods=['GET'])
def displayListeDePrixFor():
    if session['id'] == None:
        return signin()
    table = "panneaux"
    title = "Panneaux"
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(headersData, table, "Catégorie, Hauteur, Largeur")
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
        return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions)
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId=table, soumissions=soumissions)


@listeDePrix.route("/listeDePrix/ferronnerie", methods=['GET'])
def displayListeDePrixFor():
    if session['id'] == None:
        return signin()
    table = "ferronnerie"
    title = "Ferronnerie"
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(headersData, table, "Catégorie, Hauteur, Largeur")
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
        return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions)
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId=table, soumissions=soumissions)

    

@listeDePrix.route("/listeDePrix/search", methods=['GET'])
def index():
    if session['id'] == None:
        return signin()
    search_term = request.args.get('search', '')
    product = request.args.get('product', '')
    title = request.args.get('title')
    headersData = getHeaders(product)
    soumissions = getSoumissions(session["id"])
    if search_term:
        cmd = getCmdWithHeadersWithSearch(headersData,product, search_term)
    else:
        cmd = getCmdWithHeaders(headersData, product, "Catégorie, Hauteur, Largeur")
    cur=conn.cursor()
    cur.execute(cmd)
    tableData = cur.fetchall()
    cur.close()
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=tableData, soumissions=soumissions)


@listeDePrix.route("/listeDePrix/orderBy", methods=['GET'])
def displayListeDePrixForOrderBy():
    if session['id'] == None:
        return signin()
    orderBy = request.form.get('orderBy')
    table = request.form.get('table')
    title = request.form.get('title')
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(headersData, table, orderBy)
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
    qty = request.form.get('qty', type=int)
    soumissionID = request.form.get('soumissionID')
    productID = request.form.get('productID', type=int)
    table = request.form.get('table')
    title = request.form.get('title')
    try:
        tableToAdd : str
        tableToAdd = getTableToAddItem(productID)
        if tableToAdd == "":
            print("ERROR")
            return displayListeDePrixFor(table, title)
        print(tableToAdd)
        print(soumissionID)
        print(productID)
        print(qty)
        cmd = 'INSERT INTO '+ str(tableToAdd) +' (sID, ProductID, sQuantite) VALUES (\''+soumissionID+'\', '+ str(productID) +', '+ str(qty) +');'
        print(cmd)
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
        
    return displayListeDePrixFor(table, title)


def getTableToAddItem(itemID):
   cmd = 'SELECT produit FROM produits WHERE ID_Produit = '+str(itemID)+';'
   cur.execute(cmd)
   conn.commit()
   table = cur.fetchone()[0]
   
   match table:
       case 'porte':
           return 'soumission_asso_porte'
       case 'panneaux':
           return 'soumission_asso_panneaux'
       case 'ferronnerie':
           return 'soumission_asso_ferronnerie'

   return table

def getHeaders(table):
    try:
        cmd='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \''+table+'\' AND (COLUMN_KEY = \'\' OR COLUMN_KEY = \'PRI\') ORDER BY ORDINAL_POSITION;'
        cur=conn.cursor()
        cur.execute(cmd)
        headersData = [row[0] for row in cur.fetchall()]
        return headersData
    except Exception as e:
        print(e)
    return

def getCmdWithHeaders(headersData, table):
    headers = str.join(", ",headersData)
    return 'SELECT ' + headers + 'FROM' + table + ';'

def getCmdWithHeaders(headersData, table, orderBy):
    headers = str.join(",",headersData)
    return 'SELECT ' + headers + ' FROM ' + table +' ORDER BY '+ orderBy + ';'

def getCmdWithHeadersWithSearch(headersData, table, search_term, orderBy = ""):
    headers = str.join(",",headersData)
    if orderBy == "":
        return 'SELECT '+ headers + ' FROM '+ table + ' WHERE Catégorie LIKE \'%' + search_term + '%\''
    else:
        return 'SELECT ' + headers + ' FROM ' + table +' WHERE Catégorie LIKE \'%' + search_term + '%\' ORDER BY '+ orderBy + ';'

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

