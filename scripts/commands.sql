SELECT * FROM soumission_asso_panneaux NATURAL RIGHT OUTER JOIN soumission_asso_porte; AS sp ON p.sID = sp.sID; WHERE sID = "testLocal";

DECLARE PID TABLE (id varchar(24)) = (SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal");


SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal"

CREATE VIEW 

DECLARE @PID TABLE (id varchar(24));
INSERT INTO @id (id)
SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal";



SELECT TAG FROM porte WHERE ID IN SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal" 
UNION ALL SELECT TAG FROM panneaux WHERE ID IN SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal" 
UNION ALL SELECT TAG FROM ferronnerie WHERE ID IN SELECT ProductID FROM soumission_asso_panneaux UNION ALL SELECT ProductID FROM soumission_asso_porte UNION ALL SELECT ProductID FROM soumission_asso_ferronnerie WHERE sID = "testLocal";


SELECT ProductID, TAG, catégorie, prix, sQuantite, sTotal
FROM (
    SELECT TAG, ID AS ProductID , prix, catégorie, sQuantite, sTotal FROM soumission_asso_porte d INNER JOIN porte p ON d.ProductID = p.ID UNION ALL
    SELECT TAG, ID AS ProductID , prix, catégorie, sQuantite, sTotal FROM soumission_asso_panneaux d INNER JOIN panneaux p ON d.ProductID = p.ID UNION ALL
    SELECT TAG, ID AS ProductID , prix, catégorie, sQuantite, sTotal FROM soumission_asso_ferronnerie d INNER JOIN ferronnerie p ON d.ProductID = p.ID
) AS products
WHERE ProductID IN (
    SELECT ProductID FROM soumission_asso_panneaux WHERE sID = 'trest' UNION ALL
    SELECT ProductID FROM soumission_asso_porte WHERE sID = 'trest' UNION ALL
    SELECT ProductID FROM soumission_asso_ferronnerie
    WHERE sID = 'trest'
);

SELECT * FROM soumission_asso_porte d INNER JOIN porte p ON d.ProductID = p.ID;
SELECT * FROM soumission_asso_panneaux d INNER JOIN panneaux p ON d.ProductID = p.ID;
SELECT * FROM soumission_asso_ferronnerie d INNER JOIN ferronnerie p ON d.ProductID = p.ID;

INSERT INTO soumission_ids Values ("testLocal");
INSERT INTO soumission_asso_panneaux (sID, ProductID, sQuantite) Values ("testLocal", "PANNE-1", 2);
INSERT INTO soumission_asso_porte (sID, ProductID, sQuantite) Values ("testLocal", "PORTE-1", 2);
INSERT INTO soumission_asso_ferronnerie (sID, ProductID, sQuantite) Values ("testLocal", "FERRO-1", 2);
DELETE FROM soumission_asso_panneaux WHERE sID = "testLocal";

-- INSERT INTO soumission_ids VALUES ("Soumission_1");
-- INSERT INTO soumission VALUES ("Soumission_1", "PORTE-1","CABANON", 800);

-- DELETE FROM soumission_ids WHERE ID = 'Soumission_1';