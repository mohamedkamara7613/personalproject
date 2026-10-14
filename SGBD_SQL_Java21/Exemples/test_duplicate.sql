-- Création de la table initiale
CREATE TABLE users (id INT, name VARCHAR);
-- Insertion des données test
INSERT INTO users (id, name) VALUES (1, "Alice");
INSERT INTO users (id, name) VALUES (2, "Bob");
-- Test de détection de doublon (doit échouer)
CREATE TABLE users (temp INT);
-- Vérification finale
SELECT * FROM users;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table users créée.
-- > 1 ligne insérée dans users
-- > 1 ligne insérée dans users
-- > Erreur: La table users existe déjà.
-- > Table: users
-- | id              | name            |
-- |-----------------|-----------------|
-- | 1               | Alice           |
-- | 2               | Bob             |
-- 
-- > Au revoir !
