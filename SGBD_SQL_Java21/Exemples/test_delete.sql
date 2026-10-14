CREATE TABLE test_del (id SERIAL, nom VARCHAR, age INT);
INSERT INTO test_del (nom, age) VALUES ("Alice", 25);
INSERT INTO test_del (nom, age) VALUES ("Bob", 30);
INSERT INTO test_del (nom, age) VALUES ("Charlie", 35);
SELECT * FROM test_del;
-- Delete Charlie
DELETE FROM test_del WHERE age > 30;
SELECT * FROM test_del;
-- Delete everyone
DELETE FROM test_del;
SELECT * FROM test_del;
DROP TABLE test_del;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table test_del créée.
-- > 1 ligne insérée dans test_del
-- > 1 ligne insérée dans test_del
-- > 1 ligne insérée dans test_del
-- > Table: test_del
-- | id              | nom             | age             |
-- |-----------------|-----------------|-----------------|
-- | 1               | Alice           | 25              |
-- | 2               | Bob             | 30              |
-- | 3               | Charlie         | 35              |
-- 
-- > 1 ligne(s) supprimée(s) de test_del
-- > Table: test_del
-- | id              | nom             | age             |
-- |-----------------|-----------------|-----------------|
-- | 1               | Alice           | 25              |
-- | 2               | Bob             | 30              |
-- 
-- > 2 ligne(s) supprimée(s) de test_del
-- > Table: test_del
-- | id              | nom             | age             |
-- |-----------------|-----------------|-----------------|
-- 
-- > Table test_del supprimée.
-- > Au revoir !
