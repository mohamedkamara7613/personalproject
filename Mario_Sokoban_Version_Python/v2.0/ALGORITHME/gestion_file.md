
---

# **README - gestion_file.py**

## **Description globale**
Le fichier `gestion_file.py` gère la **lecture** et l'**écriture** des niveaux dans le jeu Mario Sokoban v2.0.  
Son rôle est de :
1. Charger les niveaux depuis un fichier binaire (`level.lvl`).
2. Sauvegarder les niveaux créés ou modifiés par l'utilisateur.
3. Assurer la persistance des données des niveaux entre les sessions.

Il utilise le module **`pickle`** pour sérialiser et désérialiser les données, ainsi que **`os`** pour vérifier l'existence des fichiers.

---

## **Fonctionnalités principales**

### **1. Fonction `load_level(niveau)`**
#### **Rôle :**
- Charge un niveau spécifique à partir du fichier binaire `level.lvl`.
- Remplit la grille du jeu (`grille`) avec les données correspondantes.

#### **Étapes détaillées :**
1. **Vérification du fichier `level.lvl` :**
   - Si le fichier n'existe pas, il est créé avec les niveaux par défaut (`niveaux`).

   ```python
   if not os.path.exists("doc/level.lvl"):
       with open("doc/level.lvl", "wb") as file:
           record = pickle.Pickler(file)
           record.dump(niveaux)
   ```

2. **Chargement des niveaux :**
   - Ouvre le fichier `level.lvl` en mode binaire et charge le dictionnaire des niveaux avec `pickle`.

   ```python
   with open("doc/level.lvl", "rb") as file:
       get_record = pickle.Unpickler(file)
       niveaux = get_record.load()
   ```

3. **Validation de l'indice du niveau :**
   - Si l'indice demandé est supérieur au dernier niveau disponible, retourne `76` (code spécifique).
   - Si l'indice est négatif, il est remis à `0`.

4. **Décodage des données du niveau :**
   - La chaîne représentant le niveau est convertie en une grille bidimensionnelle où chaque chiffre correspond à un objet du jeu.

   Exemple pour une ligne :
   ```python
   if line[(i * nb_bloc_width) + j] == '0':
       grille[i][j] = 0
   ```

5. **Retour en cas d'erreur :**
   - Si le fichier est introuvable, retourne `False`.

---

### **2. Fonction `save_level(grille)`**
#### **Rôle :**
- Sauvegarde la grille actuelle comme un nouveau niveau dans le fichier `level.lvl`.

#### **Étapes détaillées :**
1. **Chargement des niveaux existants :**
   - Charge le dictionnaire `niveaux` depuis `level.lvl`.

2. **Génération d'une nouvelle clé pour le niveau :**
   - Trouve la dernière clé existante et l'incrémente pour ajouter le nouveau niveau.

   ```python
   for key in niveaux:
       niveau = key
   niveau += 1
   ```

3. **Encodage de la grille :**
   - Parcourt la grille bidimensionnelle et la convertit en une chaîne linéaire.
   - Ajoute cette chaîne au dictionnaire des niveaux.

   ```python
   line = line + str(grille[i][j])
   niveaux[niveau] = line
   ```

4. **Écriture des niveaux dans le fichier :**
   - Sérialise et écrit le dictionnaire mis à jour dans `level.lvl`.

   ```python
   with open("doc/level.lvl", "wb") as file:
       record = pickle.Pickler(file)
       record.dump(niveaux)
   ```

5. **Retour en cas d'erreur :**
   - Si le fichier est introuvable, retourne `False`.

---

## **Technologies et techniques utilisées**

1. **Sérialisation avec `pickle` :**
   - Permet de sauvegarder et de charger des objets Python complexes (comme les dictionnaires) sous forme binaire.

2. **Manipulation de fichiers avec `os` :**
   - Vérifie l'existence des fichiers pour éviter les erreurs lors de la lecture ou de l'écriture.

3. **Encodage des niveaux :**
   - Les niveaux sont représentés comme des chaînes de caractères compactes. Chaque chiffre dans la chaîne correspond à un type d'objet (mur, caisse, joueur, etc.).

4. **Grille bidimensionnelle :**
   - La conversion entre la grille et la chaîne est essentielle pour stocker efficacement les niveaux dans un fichier.

---

## **Détails importants pour une transcription ou un recodage**

1. **Sérialisation :**
   - Si vous passez à un autre langage, utilisez une technologie équivalente à `pickle` pour sérialiser les niveaux (par exemple, JSON ou protobuf).

2. **Structure des niveaux :**
   - Conservez le format compact des niveaux (chaînes linéaires), mais documentez la correspondance entre les chiffres et les objets pour éviter toute confusion.

3. **Gestion des erreurs :**
   - Prévoir des mécanismes robustes pour gérer les fichiers manquants ou corrompus.

4. **Encodage et décodage :**
   - Les étapes de conversion entre la grille et la chaîne sont essentielles pour la compatibilité. Veillez à implémenter cette logique avec précision dans d'autres environnements.

---

## **Exemple d'utilisation**

### **Charger un niveau**
```python
niveau = 1
if load_level(niveau):
    print("Niveau chargé avec succès.")
else:
    print("Erreur lors du chargement du niveau.")
```

### **Sauvegarder un niveau**
```python
# Exemple de grille bidimensionnelle
grille = [[0, 1, 2], [3, 4, 5], [0, 0, 1]]
if save_level(grille):
    print("Niveau sauvegardé avec succès.")
else:
    print("Erreur lors de la sauvegarde du niveau.")
```

---

## **Améliorations possibles**

1. **Validation des niveaux :**
   - Ajouter une vérification pour s’assurer que les grilles chargées ou sauvegardées respectent les dimensions définies (`nb_bloc_width`, `nb_bloc_height`).

2. **Compatibilité multiplateforme :**
   - Envisager un format plus universel, comme JSON, pour les niveaux au lieu de `pickle`.

3. **Interface utilisateur :**
   - Ajouter une option dans le jeu pour afficher et sélectionner les niveaux disponibles.

---
