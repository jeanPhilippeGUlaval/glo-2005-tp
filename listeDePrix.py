from flask import Flask, render_template, request, Blueprint, session
from database import conn, cur
import pymysql
import logging
import pymysql.cursors
import os
from dotenv import load_dotenv


listeDePrix = Blueprint('listeDePrix', __name__, template_folder='templates')

# @listeDePrix.route("/listeDePrix")
# def displayListeDePrix():
#     return displayListeDePrixFor()

@listeDePrix.route("/listeDePrix", methods=['GET'])
def displayListeDePrixFor(table ="", title=""):
    table : str
    title : str
    if table == None or table == "":
        table = request.args.get('table')
    if title == None or title == "":
        title = request.args.get('title')
    headersData = getHeaders(table)
    soumissions = getSoumissions(session["id"])
    cmd = getCmdWithHeaders(headersData, table, "Catégorie, Hauteur, Largeur")
    try:
        if cmd == "":
            cmd = "SELECT * FROM porte;"
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
        return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions)
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId=table, soumissions=soumissions)


@listeDePrix.route("/listeDePrix/orderBy", methods=['GET'])
def displayListeDePrixForOrderBy():
    orderBy : str
    orderBy = request.args.get('orderBy')
    table : str
    title : str
    table = request.args.get('table')
    title = request.args.get('title')
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
    qty = request.form.get('qty', type=int)
    soumissionID = request.form.get('soumissionID')
    productID = request.form.get('productID')
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
        cmd = 'INSERT INTO '+ str(tableToAdd) +' (sID, ProductID, sQuantite) VALUES (\''+soumissionID+'\', \''+ productID +'\', '+ str(qty) +');'
        print(cmd)
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
        
    return displayListeDePrixFor(table, title)


def getTableToAddItem(itemID):
    itemType = str.split(itemID, "-")[0]
    if itemType == "PORTE":
        return 'soumission_asso_porte'
    elif itemType == "FERRO":
        return 'soumission_asso_ferronnerie'
    elif itemType == "PANNE":
        return 'soumission_asso_panneaux'
    else:
        return ""

def getHeaders(table):
    try:
        cmd='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \''+table+'\' AND (COLUMN_KEY = \'\' OR COLUMN_KEY = \'PRI\');'
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

