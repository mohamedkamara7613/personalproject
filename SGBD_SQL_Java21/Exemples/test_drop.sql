CREATE TABLE test_drop (id SERIAL, nom VARCHAR);
INSERT INTO test_drop (nom) VALUES ("Batman");
SELECT * FROM test_drop;
DROP TABLE test_drop;
-- This should fail if the table was correctly dropped
SELECT * FROM test_drop;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table test_drop créée.
-- > 1 ligne insérée dans test_drop
-- > Table: test_drop
-- | id              | nom             |
-- |-----------------|-----------------|
-- | 1               | Batman          |
-- 
-- > Table test_drop supprimée.
-- > Erreur: Table inconnue : test_drop
-- > Au revoir !
