from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'votre_utilisateur'
app.config['MYSQL_PASSWORD'] = 'votre_mot_de_passe'
app.config['MYSQL_DB'] = 'nom_de_votre_base_de_donnees'

mysql = MySQL(app)

@app.route('/')
def index():
    search_term = request.args.get('search', '')
    cur = mysql.connection.cursor()
    if search_term:
        cur.execute("SELECT * FROM produits WHERE type_produit LIKE %s", ('%' + search_term + '%',))
    else:
        cur.execute("SELECT * FROM produits")
    produits = cur.fetchall()
    cur.close()
    return render_template('index.html', produits=produits)

@app.route('/ajouter_produit', methods=['POST'])
def ajouter_produit():
    if request.method == 'POST':
        details_produit = request.form
        type_produit = details_produit['type_produit']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM produits WHERE type_produit = %s", (type_produit,))
        produit_existe = cur.fetchone()
        if produit_existe:
            cur.execute("UPDATE produits SET nombre_modifications = nombre_modifications + 1 WHERE type_produit = %s", (type_produit,))
        else:
            cur.execute("INSERT INTO produits (type_produit) VALUES (%s)", (type_produit,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
