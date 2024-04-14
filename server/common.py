from database import *


# Fonction qui retourne la liste des soumissions de l'utilisateur actif.
def getOpenSoumissionList():
    tableData = ""
    try:
        cmd = 'SELECT * FROM soumission_ids WHERE userID = ' + str(session["id"]) + ' AND envoye = 0;'
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(e)
    return tableData

def getAllSoumissionList():
    tableData = ""
    try:
        cmd = 'SELECT * FROM soumission_ids WHERE userID = ' + str(session["id"]) +';'
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(e)
    return tableData

# Cette fonction nous permet d'aller chercher les titre de colonne d'une table. Cela nous permet donc
# d'être dynamique sur l'affichage en HTML que l'on produit. On envoi ensuite les titres de colonnes
# à la page HTML. Cela permet aussi de diminuer la quantité de code à faire à chaque fois qu'on rajoute
# une table de produit.
def getHeaders(table):
    headersData = ""
    try:
        cmd='SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = \''+table+'\' ORDER BY ORDINAL_POSITION;'
        cur=conn.cursor()
        cur.execute(cmd)
        headersData = [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(e)
    return headersData
