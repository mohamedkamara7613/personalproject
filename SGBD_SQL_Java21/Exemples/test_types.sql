CREATE TABLE TableA (id SERIAL, nom VARCHAR);
CREATE TABLE TableB (id SERIAL, label VARCHAR);
INSERT INTO TableA (nom) VALUES ("Zebra");
INSERT INTO TableB (label) VALUES ("Apple");
INSERT INTO TableA (nom) VALUES ("Banana");
SELECT * FROM TableA;
SELECT * FROM TableB;
SELECT * FROM TableA WHERE nom > "Apple";
SELECT * FROM TableA WHERE nom < "Zebra";
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table TableA créée.
-- > Table TableB créée.
-- > 1 ligne insérée dans TableA
-- > 1 ligne insérée dans TableB
-- > 1 ligne insérée dans TableA
-- > Table: TableA
-- | id              | nom             |
-- |-----------------|-----------------|
-- | 1               | Zebra           |
-- | 3               | Banana          |
-- 
-- > Table: TableB
-- | id              | label           |
-- |-----------------|-----------------|
-- | 2               | Apple           |
-- 
-- > Table: TableA_selection
-- | id              | nom             |
-- |-----------------|-----------------|
-- | 1               | Zebra           |
-- | 3               | Banana          |
-- 
-- > Table: TableA_selection
-- | id              | nom             |
-- |-----------------|-----------------|
-- | 3               | Banana          |
-- 
-- > Au revoir !
