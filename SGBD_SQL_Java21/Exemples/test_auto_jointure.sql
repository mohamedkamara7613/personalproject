CREATE TABLE employes (id INT, nom VARCHAR, manager_id INT);
INSERT INTO employes (id, nom, manager_id) VALUES (1, "Bruce Wayne", 0);
INSERT INTO employes (id, nom, manager_id) VALUES (2, "Alfred Pennyworth", 1);
INSERT INTO employes (id, nom, manager_id) VALUES (3, "Dick Grayson", 1);
INSERT INTO employes (id, nom, manager_id) VALUES (4, "Jason Todd", 3);

TABLES;
SELECT * FROM employes;

-- Auto-jointure pour trouver le nom du manager de chaque employé
-- Note: Alfred et Dick ont Bruce (id=1) comme manager. Jason a Dick (id=3).
SELECT E.nom, M.nom FROM employes E, employes M WHERE E.manager_id = M.id;

-- Test avec le mot-clé AS
SELECT E.nom, M.nom FROM employes AS E, employes AS M WHERE E.manager_id = M.id;

DROP TABLE employes;
EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table employes créée.
-- > 1 ligne insérée dans employes
-- > 1 ligne insérée dans employes
-- > 1 ligne insérée dans employes
-- > 1 ligne insérée dans employes
-- > Tables disponibles :
-- - employes
-- 
-- > Table: employes
-- | id              | nom             | manager_id      |
-- |-----------------|-----------------|-----------------|
-- | 1               | Bruce Wayne     | 0               |
-- | 2               | Alfred Pennyworth | 1               |
-- | 3               | Dick Grayson    | 1               |
-- | 4               | Jason Todd      | 3               |
-- 
-- > Table: E_M_selection_projection
-- | E.nom           | M.nom           |
-- |-----------------|-----------------|
-- | Alfred Pennyworth | Bruce Wayne     |
-- | Dick Grayson    | Bruce Wayne     |
-- | Jason Todd      | Dick Grayson    |
-- 
-- > Table: E_M_selection_projection
-- | E.nom           | M.nom           |
-- |-----------------|-----------------|
-- | Alfred Pennyworth | Bruce Wayne     |
-- | Dick Grayson    | Bruce Wayne     |
-- | Jason Todd      | Dick Grayson    |
-- 
-- > Table employes supprimée.
-- > Au revoir !
