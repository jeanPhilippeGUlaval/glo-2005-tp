CREATE DATABASE dev;
USE dev;
CREATE TABLE users(ID int PRIMARY KEY AUTO_INCREMENT, email varchar(256) UNIQUE, password varchar(64), salt varchar(32));
CREATE INDEX email_index on users(email);

CREATE TABLE forgottenPassword(email varchar(256) UNIQUE, token int);
CREATE INDEX email_index on forgottenPassword(email)

CREATE TABLE produits(ID INT AUTO_INCREMENT PRIMARY KEY, TAG VARCHAR(70), Catégorie varchar(30), prix int);
CREATE FULLTEXT INDEX categorie_fulltext_index ON produits(Catégorie);

CREATE TABLE porte (ID int, Largeur int, Hauteur int, isolation varchar(4), Motif int, Ferronerie varchar(24), Alliage varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);
CREATE TABLE panneaux(ID int, Largeur int, Hauteur int, isolation varchar(4), Modele varchar(255), Alliage varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);
CREATE TABLE ferronnerie(ID int, Largeur int, Hauteur int, Diametre varchar(6), Type varchar(24), FOREIGN KEY (ID) REFERENCES produits(ID) ON DELETE CASCADE);

CREATE TABLE soumission_ids (ID VARCHAR(24) PRIMARY KEY, userID int, dateSoumission TIMESTAMP DEFAULT CURRENT_TIMESTAMP, envoye int DEFAULT (0), FOREIGN KEY(userID) REFERENCES users(ID) ON DELETE CASCADE);
CREATE INDEX envoye_index ON soumission_ids(envoye);
CREATE INDEX usersID_index ON soumission_ids(usersID);


CREATE TABLE soumission_asso_produits(sID VARCHAR(24),
ProductID int NOT NULL,
sQuantite int NOT NULL,
sTotal DECIMAL,
FOREIGN KEY (ProductID) REFERENCES produits(ID) ON DELETE CASCADE,
FOREIGN KEY (sID) REFERENCES soumission_ids(ID) ON DELETE CASCADE);
CREATE INDEX ProductID_index_SAP ON soumission_asso_produits(ProductID);
CREATE INDEX sID_index_SAP ON soumission_asso_produits(sID);

/*
    Cette Procédure s'occupe d'ajouter des items dans la table d'association de soumission avec produit.
    Sa logique est de vérifier si le produit est déjà présent dans la soumission, si oui, elle ajoute la nouvelle quantité
    et recalcule son total, sinon elle rajoute le nouveau produit dans la table. 
*/
DELIMITER //
CREATE PROCEDURE AjouterSoumission(IN param_produitID int, IN qty int,IN soumissionID varchar(24))
BEGIN
    DECLARE total DECIMAL;    
    -- On viens sélectionner le produit dans la table de soumission et si il retourne rien, 
    -- on vient l'ajouter, sinon on met à jour la table avec les nouvelles valeurs.
    IF EXISTS (SELECT * FROM soumission_asso_produits WHERE ProductID = param_produitID AND sID = soumissionID) THEN
        -- Ici on viens chercher la quantité du produits dans la table ainsi que son prix unitaire.
        CREATE TEMPORARY TABLE temp_table AS SELECT s.sQuantite, p.prix FROM soumission_asso_produits s INNER JOIN (SELECT ID, prix from produits WHERE ID = param_produitID) p ON p.ID = s.ProductID WHERE s.ProductID = param_produitID AND s.sID = soumissionID;
        -- On viens additionner l'ancienne quantité avec la nouvelle.
        SET @NewQty = qty +  (SELECT sQuantite FROM temp_table);
        -- Ajuste le prix avec le prix unitaire actuel (Si le prix change pendant que l'utilisateur crée sa soumission, celui-ci sera mis à jour)
        SET total = @NewQty * (SELECT prix FROM temp_table);
        -- On viens mettre à jour la table avec la nouvelle quantité et le nouveau prix total
        UPDATE soumission_asso_produits SET sQuantite = @NewQty, sTotal = total WHERE ProductID = param_produitID AND sID = soumissionID ;
        DROP TEMPORARY TABLE temp_table;
    ELSE
        -- Si le produit n'existe pas déjà dans la table de soumission, on 
        -- viens chercher son prix unitaire actuel et fait simplement l'ajouter dans la table de soumission
        SET total = qty * (SELECT prix FROM produits WHERE ID = param_produitID);
        INSERT INTO soumission_asso_produits (sID, ProductID, sQuantite, sTotal) VALUES (soumissionID, param_produitID, qty, total);
    END IF;
END //
DELIMITER ;
/*
    Les procédures suivantes permettent d'ajouter un nouveau produit dans la table de spécialisation. Étant des spécialisation
    de produits, nous devons avoir une procédure afin de remplir les deux tables avec les bonnes informations.
*/
DELIMITER //
CREATE PROCEDURE AjouterPorte(IN categorie varchar(30), IN largeur int, IN hauteur int,IN isolation varchar(4),IN Motif int,IN Ferronerie varchar(24),IN Alliage varchar(24),IN prix int)
BEGIN
    -- On ajoute le tag qui représente la table correspondante, la catégorie de produits ainsi que le prix. 
    -- l'ID est généré automatiquement.
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("porte",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    -- On prend l'ID crée et l'ajoutons dans la table porte (spécialisation)
    INSERT INTO porte VALUES (@id_produit, largeur, hauteur, isolation, Motif, Ferronerie, Alliage);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterPanneaux(IN categorie varchar(30), IN largeur int, IN hauteur int,IN isolation varchar(4),IN Modele varchar(255),IN Alliage varchar(24),IN prix int)
BEGIN
    -- On ajoute le tag qui représente la table correspondante, la catégorie de produits ainsi que le prix. 
    -- l'ID est généré automatiquement.
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("panneaux",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    -- On prend l'ID crée et l'ajoutons dans la table panneaux (spécialisation)
    INSERT INTO panneaux VALUES (@id_produit, largeur, hauteur, isolation, Modele, Alliage);
END//
DELIMITER ;

DELIMITER //
CREATE PROCEDURE AjouterFerronnerie(IN categorie varchar(30), IN largeur int, IN hauteur int,IN Diametre varchar(6),IN Type varchar(24),IN prix int)
BEGIN
    -- On ajoute le tag qui représente la table correspondante, la catégorie de produits ainsi que le prix. 
    -- l'ID est généré automatiquement.
    INSERT INTO produits (TAG, catégorie, prix) VALUES ("ferronnerie",categorie, prix);
    SET @id_produit = LAST_INSERT_ID();
    -- On prend l'ID crée et l'ajoutons dans la table ferronnerie (spécialisation)
    INSERT INTO ferronnerie VALUES (@id_produit, largeur, hauteur, Diametre, Type);
END//
DELIMITER ;
/*
    Fin des procédures de création de spécialisation, créer de nouvelle procédure si on ajoute de nouveau produits.
*/
