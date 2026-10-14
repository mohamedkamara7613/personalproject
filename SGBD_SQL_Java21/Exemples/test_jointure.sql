CREATE TABLE auteurs (id INT, nom VARCHAR, nationalite VARCHAR);
INSERT INTO auteurs (id, nom, nationalite) VALUES (1, "Victor Hugo", "Français");
INSERT INTO auteurs (id, nom, nationalite) VALUES (2, "William Shakespeare", "Anglais");
INSERT INTO auteurs (id, nom, nationalite) VALUES (3, "Molière", "Français");

CREATE TABLE livres (id_livre INT, titre VARCHAR, auteur_id INT);
INSERT INTO livres (id_livre, titre, auteur_id) VALUES (101, "Les Misérables", 1);
INSERT INTO livres (id_livre, titre, auteur_id) VALUES (102, "Notre-Dame de Paris", 1);
INSERT INTO livres (id_livre, titre, auteur_id) VALUES (103, "Hamlet", 2);
INSERT INTO livres (id_livre, titre, auteur_id) VALUES (104, "Tartuffe", 3);
INSERT INTO livres (id_livre, titre, auteur_id) VALUES (105, "Le Malade Imaginaire", 3);

SELECT auteurs.nom, livres.titre FROM auteurs, livres WHERE auteurs.id = livres.auteur_id;
exit;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table auteurs créée.
-- > 1 ligne insérée dans auteurs
-- > 1 ligne insérée dans auteurs
-- > 1 ligne insérée dans auteurs
-- > Table livres créée.
-- > 1 ligne insérée dans livres
-- > 1 ligne insérée dans livres
-- > 1 ligne insérée dans livres
-- > 1 ligne insérée dans livres
-- > 1 ligne insérée dans livres
-- > Table: auteurs_livres_selection_projection
-- | auteurs.nom     | livres.titre    |
-- |-----------------|-----------------|
-- | Victor Hugo     | Les Misérables  |
-- | Victor Hugo     | Notre-Dame de Paris |
-- | William Shakespeare | Hamlet          |
-- | Molière         | Tartuffe        |
-- | Molière         | Le Malade Imaginaire |
-- 
-- > Au revoir !
