USE dev;
ALTER TABLE bundle_asso_color DROP CONSTRAINT bundle_asso_color_ibfk_1;
ALTER TABLE bundle_asso_color DROP CONSTRAINT bundle_asso_color_ibfk_2;
ALTER TABLE soumission DROP CONSTRAINT soumission_ibfk_1;
ALTER TABLE porte DROP CONSTRAINT porte_ibfk_1;
DROP TABLE users;
DROP TABLE color;
DROP TABLE porte;
DROP TABLE bundle;
DROP TABLE bundle_asso_color;
DROP TABLE porte_id_gen;
DROP TABLE soumission_ids;
DROP TABLE soumission;
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