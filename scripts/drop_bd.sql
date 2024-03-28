USE dev;
DROP TABLE soumission_asso_porte;
DROP TABLE soumission_asso_panneaux;
DROP TABLE soumission_asso_ferronnerie;
DROP TABLE soumission_ids;
DROP TABLE users;
DROP TABLE porte;
DROP TABLE porte_id_gen;
DROP TABLE ferronnerie;
DROP TABLE ferro_id_gen;
DROP TABLE panneaux;
DROP TABLE panneaux_id_gen;

DROP TRIGGER CalPrixTotalPanneau;
DROP TRIGGER porte_insert;
DROP TRIGGER panneau_insert;
DROP TRIGGER ferro_insert;

DROP DATABASE dev;


-- // USE THIS TO CHECK WHAT ARE THE CONSTRAINTS // -------
-- USE INFORMATION_SCHEMA;
-- SELECT TABLE_NAME,
--        COLUMN_NAME,
--        CONSTRAINT_NAME,
--        REFERENCED_TABLE_NAME,
--        REFERENCED_COLUMN_NAME
-- FROM KEY_COLUMN_USAGE
-- WHERE TABLE_SCHEMA = "dev" 
--       AND TABLE_NAME = "porte" 
--       AND REFERENCED_COLUMN_NAME IS NOT NULL;