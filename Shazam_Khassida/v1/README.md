# Shazam Khassida

Une application de reconnaissance de Khassidas basée sur une architecture hybride à deux passes :
1. **Pass 1 (Fingerprinting "Shazam-like")** : Recherche d'alignement temporel exact pour identifier rapidement des enregistrements originaux identiques, y compris avec du bruit de fond. (Basé sur la Constellation de Pics).
2. **Pass 2 (Inférence Symbolique "DTW")** : Recherche de similarité vocale pour identifier des covers, variations de tempo ou autres chants non-originaux. (Basé sur l'extraction des MFCC et la distance de Dynamic Time Warping).

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

## Structure des Cendriers de Données (Data)

Placez vos Khassidas de référence originaux dans le dossier `data/ref/`. Cette base servira de "dictionnaire" de connaissance au système.
* Chaque dossier représentera l'ID du Khassida.
* Chaque fichier `.wav` représentera la version du Khassida.

```
data/
└── ref/
    ├── Mathlaboul_Fawzayni/
    │   ├── version_originale.wav
    │   └── cover_studio.wav
    └── Mofatihoul_Bichri/
        └── version_live.wav
```

## Construire la Base de Données

```bash
python main.py build
```
Cette commande va uploader tous les Khassidas dans la base de données SQLite (Pass 1) et Pickle (Pass 2) dans un format chunké.

## Reconnaitre un Khassida Extrait du Téléphone

Les extraits audios à tester (bruités, autres chanteurs, etc.) peuvent être placés dans `data/raw/`.

```bash
python main.py recognize data/raw/mon_enregistrement_test.wav
```
