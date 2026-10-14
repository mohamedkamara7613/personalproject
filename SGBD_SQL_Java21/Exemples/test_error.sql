CREATE TABLE test_types (id INT, nom VARCHAR);
INSERT INTO test_types (id, nom) VALUES (1, "Alice");
SELECT * FROM test_types WHERE id = "Alice";
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table test_types créée.
-- > 1 ligne insérée dans test_types
-- > Erreur: Types incompatibles pour la comparaison : ENTIER et CHAINE
-- > Au revoir !
