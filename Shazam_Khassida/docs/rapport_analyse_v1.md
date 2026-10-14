# Shazam Khassida - Rapport d'Analyse (Version 1)

Ce document recense l'architecture du prototype initial (V1), les problèmes rencontrés lors des tests en conditions réelles, et une analyse technique des limites de cette approche pour la reconnaissance vocale de chants a cappella (Khassidas).

## 1. Architecture du Prototype V1

L'objectif de la V1 était de construire un moteur de reconnaissance audio composé de deux passes (Filtres) :

*   **Pass 1 (Fingerprinting - Moteur Exact) :** Inspiré de l'algorithme original de Shazam. Il génère un spectrogramme, identifie les pics d'énergie les plus forts (Constellation), et crée des paires de pics (Hashes) associées à un décalage temporel. Ces empreintes sont stockées dans une base SQLite. Le but est de trouver une correspondance *exacte* (même audio, même avec du bruit).
*   **Pass 2 (Inférence Symbolique - Moteur de Similarité) :** Si le Pass 1 échoue, le système utilise les MFCC (Mel-Frequency Cepstral Coefficients) pour extraire le "timbre vocal" et utilise l'algorithme DTW (Dynamic Time Warping) pour calculer une distance mathématique entre l'audio de la requête et la base de données. Le but est de trouver des "covers" (le même texte chanté par une autre personne, ou à une vitesse différente).

## 2. Problèmes Rencontrés en Conditions Réelles

Lors des tests avec de véritables enregistrements (des Khassidas de 30 minutes, compressés en MP3), plusieurs failles critiques ont été identifiées :

### A. Les Faux Positifs du Pass 1 (Sensibilité au Bruit de Fond)
*   **Symptôme :** N'importe quel audio (même de la musique ou un bruit aléatoire) était reconnu comme appartenant au Khassida le plus long de la base de données (ex: `midadi` qui dure 30 minutes), avec un score d'une vingtaine de points.
*   **Cause mathématique :** Le seuil de détection des pics d'amplitude était trop bas (`-40 dB`). L'algorithme capturait le "souffle" du micro, les bruits de salle, ou les interférences électriques (ex: ronflement à 50 Hz). Puisque ce bruit de fond est universel, les empreintes générées (Hashes) correspondaient au hasard et s'accumulaient statistiquement sur le fichier le plus long.
*   **Correctif V1 :** Augmentation du seuil d'amplitude à `-20 dB` et filtrage des très basses fréquences (< 100 Hz). Le taux de faux positifs a drastiquement chuté à 3 points.

### B. Les Faux Négatifs du Pass 1 (Sensibilité Phase / Encodage MP3)
*   **Symptôme :** Même en fournissant la copie exacte d'un Khassida, le Pass 1 peinait à dépasser les 10 à 38 points d'alignement (ce qui est extrêmement faible pour un fichier de 30 minutes qui génère des millions de points).
*   **Cause mathématique :** L'encodage MP3 intègre un *padding* (des millisecondes de silence ajoutées au début ou à la fin du fichier). Cela décale très légèrement la phase du signal dans le temps. L'analyse de Fourier (STFT) s'en trouve subtilement décalée. Deux fichiers audios identiques à l'oreille, mais encodés par deux bibliothèques différentes (ex: `pydub` vs `librosa`), ne génèrent pas exactement la même grille temporelle de pics. De plus, la fonction de génération de Hashes ne ciblait pas correctement le futur, gaspillant des associations sur des pics simultanés.
*   **Conclusion :** Le Pass 1 est mathématiquement parfait pour un signal *identique bit à bit*, mais s'effondre avec des variations de compression si la fenêtre d'analyse n'est pas ultra-tolérante.

### C. Limites Techniques et Surcharges (Base de Données & RAM)
*   **Symptômes :** 
    *   Erreur `too many SQL variables` lors d'une simple requête sur le Pass 1.
    *   Le processus Python "tue" l'ordinateur (Out of Memory / Gel du processeur) lors du Pass 2.
*   **Causes techniques :**
    *   **SQLite :** La requête `SELECT ... WHERE hash IN (...)` recevait des milliers de paramètres d'un coup, dépassant la limite stricte de 999 variables de SQLite. Il a fallu implémenter un système de traitement par *Batches* de 900.
    *   **Algorithme DTW (Pass 2) :** L'algorithme de calcul de distance DTW a une complexité temporelle et spatiale de $O(N \times M)$. Tenter d'aligner la requête d'un fichier entier (30 minutes) contre une base de données de 30 minutes génère une matrice de millions de cellules.
*   **Correctif V1 :** "Cropping" automatique. Le système simule l'enregistrement d'un téléphone en coupant violemment tous les audios envoyés en requête aux **15 premières secondes**.

## 3. Bilan Global et Perspectives

La Version 1 aura permis de valider des concepts de base : couper l'audio en morceaux, séparer harmoniques et percussions avec HPSS, générer des empreintes, et calculer des distances MFCC.

Cependant, il est clair qu'une approche algorithmique "dure" et purement signalétique (Shazam / DTW) n'est pas assez robuste pour résoudre la problématique principale : **Reconnaître un Khassida indépendamment du chanteur, du tempo, ou de la mauvaise qualité d'enregistrement.**

Le DTW trouve rapidement ses limites face à la très grande liberté rythmique dont font preuve les chanteurs de Khassidas (pauses respiratoires irrégulières, ornementations vocales). 

Pour une **Version 2 robuste**, le projet doit opérer un pivot vers une solution basée sur le Deep Learning (Machine Learning statistique), ce qui nécessitera la constitution préalable d'un véritable Dataset. L'analyse des besoins de cette V2 fait l'objet d'un document distinct (Cahier des Charges V2).
