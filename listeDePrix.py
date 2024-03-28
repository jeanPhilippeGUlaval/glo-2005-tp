from flask import Flask, render_template, request, Blueprint
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
def displayListeDePrixFor():
    table : str
    title : str
    table = request.args.get('table')
    title = request.args.get('title')
    headersData = getHeaders(table)
    soumissions = getSoumissions("")
    print(soumissions)
    cmd = getCmdWithHeaders(headersData, table, "Catégorie, Hauteur, Largeur")
    try:
        print(cmd)
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
    soumissions = getSoumissions("")
    cmd = getCmdWithHeaders(headersData, table, orderBy)
    try:
        print(cmd)
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data = tableData, tableId=table, soumissions=soumissions)

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
        if userID != "":
            cmd='SELECT ID FROM soumission_ids WHERE userID = ' + userID +';'
        else:
            cmd= 'SELECT ID FROM soumission_ids;'
        cur=conn.cursor()
        cur.execute(cmd)
        soumissions = [row[0] for row in cur.fetchall()]
        return soumissions
    except Exception as e:
        print(e)
    return

