# 🎯 CONTEXTE ET OBJECTIF
Tu es un Ingénieur Audio et Backend Senior. Ta mission est de construire un moteur d'identification audio de **Khassidas** (chants religieux sénégalais, très vocaux, souvent a cappella ou répétitifs). 

Nous visons un prototype de qualité production, robuste au bruit et aux variations de voix.
Nous utiliserons une **Architecture Hybride (Two-Pass Search)** :
* **Pass 1 (Fingerprinting) :** Type Shazam. Ultra-rapide, tolérant au bruit, pour retrouver un enregistrement exact.
* **Pass 2 (Similarité Vocale) :** Basé sur les MFCC et le DTW (Dynamic Time Warping). Pour identifier des reprises (covers) ou des variations de chant inédites.

---

# ⚠️ RÈGLE D'OR : MÉTHODOLOGIE TDD ET MODULAIRE
Tu ne dois **PAS** générer tout le code d'un coup. Nous allons travailler module par module. 
Pour chaque module, tu dois me fournir :
1. Le code de l'implémentation.
2. Un script de test unitaire dédié (`test_moduleX.py`).
Nous ne passerons au module suivant que lorsque je te confirmerai que le test passe sur ma machine.

---

# 🏗️ ARCHITECTURE DES MODULES (À valider un par un)

### 🔹 MODULE 1 : Pipeline de Pré-traitement et "Chunking"
Les Khassidas peuvent durer des heures. Le DTW explosera en mémoire si on ne segmente pas.
* **Fonction 1 :** Nettoyage avec `librosa` (Mono, Resampling à 16kHz, Normalisation du volume).
* **Fonction 2 :** Séparation Harmonique/Percussive (`librosa.effects.hpss`) pour isoler la voix et réduire le bruit de fond.
* **Fonction 3 :** Découpage (*Chunking*) de l'audio de référence en segments de **15 secondes** avec un chevauchement (*overlap*) de **5 secondes**. 
👉 *Action attendue : Fournis-moi le script `preprocess.py` et son test.*

### 🔹 MODULE 2 : Pass 1 - Le Moteur de Fingerprinting (Shazam-like)
Ce module gère les enregistrements exacts (même bruités).
* **Extraction :** Spectrogramme, recherche de pics locaux (`scipy.ndimage.maximum_filter`), création de paires de pics, génération de hash SHA-1 tronqués.
* **Stockage :** Base de données SQLite (`hashes.db`). Utiliser `executemany` pour les insertions par lots et créer un INDEX sur la colonne `hash` pour la rapidité.
* **Matching :** Recherche d'alignement temporel dominant (Offset = Temps Base - Temps Extrait).
👉 *Action attendue : Attends ma validation du Module 1 pour générer `fingerprint.py`, `db_sqlite.py` et le test.*

### 🔹 MODULE 3 : Pass 2 - Le Moteur de Similarité Vocale (MFCC + DTW)
Ce module prend le relais si le Pass 1 échoue. Il analyse la signature vocale.
* **Extraction :** Calcul des MFCC (Mel-Frequency Cepstral Coefficients) sur les chunks de 15s (très performant pour la voix, contrairement aux Chromagrammes).
* **Stockage :** Sauvegarde des matrices MFCC de chaque chunk dans un fichier `chunks_mfcc.pkl` (ou format similaire optimisé).
* **Matching :** Utilisation de `librosa.sequence.dtw` (ou `fastdtw` si optimisé) pour calculer la distance entre le MFCC de l'extrait utilisateur et les MFCC des chunks en base.
👉 *Action attendue : Attends ma validation du Module 2 pour générer `vocal_match.py` et le test.*

### 🔹 MODULE 4 : L'Orchestrateur Hybride (Le Moteur Principal)
Le script final `recognize.py` qui reçoit un extrait audio inconnu (10-15s).
* **Étape A :** Pré-traitement de l'extrait.
* **Étape B :** Lancement du Pass 1 (Fingerprinting).
* **Condition :** Si `score_pass_1 > seuil_confiance`, retourner le résultat immédiatement (Match Exact).
* **Étape C :** Sinon, lancer le Pass 2 (DTW sur MFCC) sur les chunks filtrés.
* **Condition :** Si `distance_dtw < seuil_tolerance`, retourner le résultat (Match Cover). Sinon, "Non reconnu".
👉 *Action attendue : Attends ma validation du Module 3 pour générer l'orchestrateur.*

---

# 🚀 INSTRUCTIONS POUR COMMENCER
Confirme que tu as compris l'architecture globale, les raisons du choix des MFCC (pour la voix) et du Chunking (pour la scalabilité). 
Ensuite, **génère uniquement le code et le test du MODULE 1** (`preprocess.py` et `test_preprocess.py`)