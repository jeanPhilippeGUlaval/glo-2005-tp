from flask import render_template, request, Blueprint, session
from database import conn, cur, TABLE_PRODUIT
from authentication import signin
from common import getHeaders, getOpenSoumissionList
import re


listeDePrix = Blueprint('listeDePrix', __name__, template_folder='templates')

# Cette fonction permet d'être générique pour tout les affichages de tables de produits.
def display(table, title, page=1):
    tableData = ""
    headersData = ""
    soumissions = ""
    # On s'assure que la table demandé fait partie des tables de produits.
    if table in TABLE_PRODUIT:
        headersData = getHeaders(table)
        soumissions = getOpenSoumissionList()
        # On s'assure que l'on ne dépasse pas les tables
        if page <= 0:
            page = 1
        cmd = getCmdWithHeaders(table, "p.Catégorie, t.Hauteur, t.Largeur", page)
        print(cmd)
        try:
            cur=conn.cursor()
            cur.execute(cmd)
            tableData = cur.fetchall()
            # Si on dépasse le nombre de page nécessaire, on revient à la page d'avant
            if len(tableData) == 0:
                return display(table, title, page-1)
            return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data=tableData, tableId=table, soumissions=soumissions, page = page)
        except Exception as e:
            print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, tableId="porte", soumissions=soumissions, page = page)

# Cette fonction envoi les données de la table porte
@listeDePrix.route("/listeDePrix/porte", methods=['GET'])
def displayListeDePrixForPorte():
    numPage = request.args.get("page", type=int)
    if numPage == None:
        numPage = 1
    if session['id'] == None:
        return signin()
    return display("porte", "Porte de Garage", numPage)

# Cette fonction envoi les données de la table panneaux
@listeDePrix.route("/listeDePrix/panneaux", methods=['GET'])
def displayListeDePrixForPanneaux():
    numPage = request.args.get("page", type=int)
    if numPage == None:
        numPage = 1
    if session['id'] == None:
        return signin()
    return display("panneaux", "Panneaux", numPage)

# Cette fonction envoi les données de la table ferronnerie
@listeDePrix.route("/listeDePrix/ferronnerie", methods=['GET'])
def displayListeDePrixForFerronnerie():
    numPage = request.args.get("page", type=int)
    if numPage == None:
        numPage = 1
    if session['id'] == None:
        return signin()
    return display("ferronnerie", "Ferronnerie", numPage)    

# Fonction qui offre la possibilité de recherché sur les catégorie du produit.
@listeDePrix.route("/listeDePrix/search", methods=['GET'])
def index():
    if session['id'] == None:
        return signin()
    search_term = request.args.get('search', '')
    # On viens enlever les caractères spéciaux et gardons seulement les caractères alphanumériques.
    # Cela permet de limiter les risques de scripts malveillants.
    search_term = re.sub(r'\W+', '', search_term)

    product = request.args.get('product', '')
    if product not in TABLE_PRODUIT:
        return display("porte", "Porte de Garage")
    
    title = request.args.get('title')
    headersData = getHeaders(product)
    soumissions = getOpenSoumissionList()
    
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

# Fonction qui place les tuples en ordre selon ce qui est demandé par l'utilisateur.
# Lorsque l'utilisateur clique sur la colonne à filtrer, on viens faire un ORDER BY sur cette colonne.
@listeDePrix.route("/listeDePrix/orderBy", methods=['GET'])
def displayListeDePrixForOrderBy():
    if session['id'] == None:
        return signin()
    orderBy = request.form.get('orderBy')
    table = request.form.get('table')
    # Si une requête malveillante est envoyé, on viens simplement retourné la table porte.
    if table not in TABLE_PRODUIT:
        return display("porte", "Porte de Garage")
    title = request.form.get('title')
    headersData = getHeaders(table)
    soumissions = getOpenSoumissionList()
    cmd = getCmdWithHeaders(table, orderBy)
    try:
        cur=conn.cursor()
        cur.execute(cmd)
        tableData = cur.fetchall()
    except Exception as e:
        print(e)
    return render_template("listeDePrix.html", lsDePrix=title, headers= headersData, data = tableData, tableId=table, soumissions=soumissions)

# Fonction qui permet d'ajouter un produit à une soumission. On reçois la requête avec les informations nécessaires:
# form: ProductID = ID du produits
# form: $ProductID-qty = quantité du produit à ajouter à la soumission
# form: soumissionID = l'identifiant de la soumission
@listeDePrix.route("/product/addToSoumission", methods=['POST'])
def addItemToSoumission():
    if session['id'] == None:
        return signin()
    productID = request.form.get('productID', type=int)
    # On viens concaténer l'identifiant produit avec -qty avec de construire la clé avec la quantité du produit
    getQty = ''+str(productID) +'-qty'
    qty = request.form.get(getQty, type=int)
    if qty <= 0:
        return
    soumissionID = request.form.get('soumissionID')
    try:
        # On appel ensuite la procédure afin d'ajouter un produit à la soumission.
        cmd = 'CALL AjouterSoumission('+str(productID)+', '+str(qty)+', \''+soumissionID+'\');'
        cur.execute(cmd)
        conn.commit()
    except Exception as e:
        print(e)
    return


# Cette fonction permet de genéré un commande SQL à partir d'information injecter.
# C'est aussi dans ces commandes qu'on gère l'injection des pages.
def getCmdWithHeaders(table, pageNumber:int):
    offset = (pageNumber - 1) * 50
    return 'SELECT p.Catégorie, t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p LIMIT 50 OFFSET '+str(offset)+';'

# Cette fonction permet de genéré un commande SQL à partir d'information injecter. OVERLOAD
def getCmdWithHeaders(table, orderBy, pageNumber:int):
    offset = (pageNumber - 1) * 50
    return 'SELECT p.Catégorie,t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p ORDER BY '+ orderBy + ' LIMIT 50 OFFSET '+str(offset)+';'

# Cette fonction permet de genéré un commande SQL à partir d'information injecter.
def getCmdWithHeadersWithSearch(table, search_term, orderBy = ""):
    if orderBy == "":
        return 'SELECT p.Catégorie, t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p WHERE p.Catégorie LIKE \'%' + search_term + '%\''
    else:
        return 'SELECT p.Catégorie,t.*, p.prix FROM ' + table + ' t NATURAL JOIN (SELECT ID, catégorie, prix FROM produits) p WHERE p.Catégorie LIKE \'%' + search_term + '%\' ORDER BY '+ orderBy + ';'

