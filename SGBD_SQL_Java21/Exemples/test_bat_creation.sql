CREATE TABLE bases (id SERIAL, nom VARCHAR, ville VARCHAR);
INSERT INTO bases (nom, ville) VALUES ("BureauInfo", "ITICity");
INSERT INTO bases (nom, ville) VALUES ("BureauElec", "ITICity");
INSERT INTO bases (nom, ville) VALUES ("BureauML", "ITICity");
INSERT INTO bases (nom, ville) VALUES ("BureauDirectionITI", "ITICity");
INSERT INTO bases (nom, ville) VALUES ("BureauDirectionLITIS", "LITISCity");

CREATE TABLE heroes (id SERIAL, nom VARCHAR, alias VARCHAR, base_id INT);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Nicola Malandain", "Batman", 1);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Nicolas Delestre", "Bikeman", 1);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Florian Yger", "Baldman", 1);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Geraldine Del Mondo", "Batgirl", 4);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Benoit Gauzere", "BGman", 3);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Clement Chatelain", "MLman", 5);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Hind Laghmara", "Resistorwoman", 2);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Laurent Vercouter", "Aquaman", 5);
INSERT INTO heroes (nom, alias, base_id) VALUES ("Robin Condat", "Robin", 2);

CREATE TABLE gadgets (id SERIAL, nom VARCHAR, hero_id INT, puissance INT);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Batarang", 6, 50);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Grappin", 6, 30);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Velo de course", 7, 40);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Casque Aero", 7, 20);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Bouclier Solaire", 8, 60);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Perruque de camouflage", 8, 10);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Ordinateur portable", 9, 80);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Moto Batgirl", 9, 70);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Lunettes de BG", 10, 90);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Parfum de charisme", 10, 100);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Neural Network Optimizer", 11, 85);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("GPU Overclocker", 11, 95);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Multimetre", 12, 45);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Resistance 10k Ohms", 12, 15);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Trident", 13, 88);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Bulle d'eau", 13, 55);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Bo staff", 14, 35);
INSERT INTO gadgets (nom, hero_id, puissance) VALUES ("Bat-cycle", 14, 65);
SELECT heroes.nom, heroes.alias, bases.ville, bases.nom, gadgets.nom 
FROM heroes, bases, gadgets 
WHERE heroes.base_id = bases.id AND gadgets.hero_id = heroes.id;

EXIT;




-- RESULTATS D'EXECUTION :
-- -----------------------
-- Student Gotham Bat Database v19.39 - Connecté à mabase
-- Tapez vos commandes SQL terminées par ';' (ou 'exit;' pour quitter)
-- > Table bases créée.
-- > 1 ligne insérée dans bases
-- > 1 ligne insérée dans bases
-- > 1 ligne insérée dans bases
-- > 1 ligne insérée dans bases
-- > 1 ligne insérée dans bases
-- > Table heroes créée.
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > 1 ligne insérée dans heroes
-- > Table gadgets créée.
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > 1 ligne insérée dans gadgets
-- > Table: heroes_bases_gadgets_selection_projection
-- | heroes.nom      | heroes.alias    | bases.ville     | bases.nom       | gadgets.nom     |
-- |-----------------|-----------------|-----------------|-----------------|-----------------|
-- | Nicola Malandain | Batman          | ITICity         | BureauInfo      | Batarang        |
-- | Nicola Malandain | Batman          | ITICity         | BureauInfo      | Grappin         |
-- | Nicolas Delestre | Bikeman         | ITICity         | BureauInfo      | Velo de course  |
-- | Nicolas Delestre | Bikeman         | ITICity         | BureauInfo      | Casque Aero     |
-- | Florian Yger    | Baldman         | ITICity         | BureauInfo      | Bouclier Solaire |
-- | Florian Yger    | Baldman         | ITICity         | BureauInfo      | Perruque de camouflage |
-- | Geraldine Del Mondo | Batgirl         | ITICity         | BureauDirectionITI | Ordinateur portable |
-- | Geraldine Del Mondo | Batgirl         | ITICity         | BureauDirectionITI | Moto Batgirl    |
-- | Benoit Gauzere  | BGman           | ITICity         | BureauML        | Lunettes de BG  |
-- | Benoit Gauzere  | BGman           | ITICity         | BureauML        | Parfum de charisme |
-- | Clement Chatelain | MLman           | LITISCity       | BureauDirectionLITIS | Neural Network Optimizer |
-- | Clement Chatelain | MLman           | LITISCity       | BureauDirectionLITIS | GPU Overclocker |
-- | Hind Laghmara   | Resistorwoman   | ITICity         | BureauElec      | Multimetre      |
-- | Hind Laghmara   | Resistorwoman   | ITICity         | BureauElec      | Resistance 10k Ohms |
-- | Laurent Vercouter | Aquaman         | LITISCity       | BureauDirectionLITIS | Trident         |
-- | Laurent Vercouter | Aquaman         | LITISCity       | BureauDirectionLITIS | Bulle d'eau     |
-- | Robin Condat    | Robin           | ITICity         | BureauElec      | Bo staff        |
-- | Robin Condat    | Robin           | ITICity         | BureauElec      | Bat-cycle       |
-- 
-- > Au revoir !
