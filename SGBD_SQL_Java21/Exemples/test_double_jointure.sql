-- Script de test pour double jointure (3 tables)
-- Tables : Etudiants, Matieres, Notes

CREATE TABLE Etudiants (id INT, nom VARCHAR);
INSERT INTO Etudiants (id, nom) VALUES (1, "Alice");
INSERT INTO Etudiants (id, nom) VALUES (2, "Bob");

CREATE TABLE Matieres (id INT, titre VARCHAR);
INSERT INTO Matieres (id, titre) VALUES (101, "SGBD");
INSERT INTO Matieres (id, titre) VALUES (102, "Algorithmique");

CREATE TABLE Notes (etudiant_id INT, matiere_id INT, valeur INT);
-- Alice a 18 en SGBD
INSERT INTO Notes (etudiant_id, matiere_id, valeur) VALUES (1, 101, 18);
-- Bob a 15 en SGBD
INSERT INTO Notes (etudiant_id, matiere_id, valeur) VALUES (2, 101, 15);
-- Alice a 20 en Algo
INSERT INTO Notes (etudiant_id, matiere_id, valeur) VALUES (1, 102, 20);

-- Requête de double jointure pour voir les noms, les matières et les notes
SELECT Etudiants.nom, Matieres.titre, Notes.valeur 
FROM Etudiants, Matieres, Notes 
WHERE Etudiants.id = Notes.etudiant_id AND Matieres.id = Notes.matiere_id;

SELECT E.nom, M.titre, N.valeur 
FROM Etudiants as E, Matieres as M, Notes as N 
WHERE E.id = N.etudiant_id AND M.id = N.matiere_id;

EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table Etudiants créée.
-- > 1 ligne insérée dans Etudiants
-- > 1 ligne insérée dans Etudiants
-- > Table Matieres créée.
-- > 1 ligne insérée dans Matieres
-- > 1 ligne insérée dans Matieres
-- > Table Notes créée.
-- > 1 ligne insérée dans Notes
-- > 1 ligne insérée dans Notes
-- > 1 ligne insérée dans Notes
-- > Table: Etudiants_Matieres_Notes_selection_projection
-- | Etudiants.nom   | Matieres.titre  | Notes.valeur    |
-- |-----------------|-----------------|-----------------|
-- | Alice           | SGBD            | 18              |
-- | Alice           | Algorithmique   | 20              |
-- | Bob             | SGBD            | 15              |
-- 
-- > Table: E_M_N_selection_projection
-- | E.nom           | M.titre         | N.valeur        |
-- |-----------------|-----------------|-----------------|
-- | Alice           | SGBD            | 18              |
-- | Alice           | Algorithmique   | 20              |
-- | Bob             | SGBD            | 15              |
-- 
-- > Au revoir !
