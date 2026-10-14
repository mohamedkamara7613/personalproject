# 🗄️ SGBD SQL Engine — Moteur Relationnel from Scratch en Java 21

[![Language](https://img.shields.io/badge/Language-Java_21_LTS-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://www.oracle.com/java/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean_SOLID-blue?style=for-the-badge)](./docs)
[![Build](https://img.shields.io/badge/Build-Makefile_&_Scripts-lightgrey?style=for-the-badge)](./makefile)

Conception et implémentation intégrale d'un **système de gestion de base de données relationnelle (SGBD-R)** en **Java 21**, sans aucun framework externe ni dépendance tierce.  
Projet académique d'excellence à l'**INSA Rouen Normandie** (Département ISIA).

---

## 🎬 Démonstration d'Exécution en Terminal

![SGBD Demo](./docs/demo_sgbd.gif)
*Démonstration de l'interpréteur SQL interactif : création de tables, insertion en mémoire, et requêtage relationnel avec projections et filtres.*

---

## 🏛️ Architecture du Moteur

```
                Requête SQL (String)
                         │
                         ▼
        [   Analyseur Syntaxique JavaCC   ] ──► Grammaire LL(1) 'sgbd.jj'
                         │
                         ▼
        [     Arbre Syntaxique (AST)      ] ──► Pattern Command
                         │
                         ▼
        [     Moteur d'Exécution / Query   ] ──► Algèbre relationnelle (Select, Project, Join)
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
   [ Buffer Pool LRU ]       [ Indexation B-Tree ]
            │                         │
            ▼                         ▼
    Fichiers Binaires (.db / pages sur disque)
```

### 1. Parseur SQL JavaCC (`sgbd.jj`)
- Grammaire LL(1) sans ambiguïté compilée via JavaCC.
- Support du DDL : `CREATE TABLE`, `DROP TABLE`.
- Support du DML : `INSERT INTO`, `DELETE FROM`, `SELECT` avec clauses `WHERE` complexes (opérateurs `=, !=, <, >, <=, >=`, connecteurs logiques `AND/OR`), projections d'attributs et **jointures multi-tables** (produit cartésien optimisé).

### 2. Couche de Stockage & Buffer Pool
- **Pages binaires :** Les tuples sont sérialisés dans des blocs disques de taille fixe avec en-tête (slotted-page architecture).
- **Buffer Manager LRU :** Mémoire cache limitant les entrées/sorties physiques disques en maintenant les pages les plus fréquemment accédées en RAM.

---

## 🚀 Utilisation & Tests

```bash
# Compiler le lexeur/parseur JavaCC et les sources Java
make

# Lancer la suite de tests unitaires JUnit
make test
```
