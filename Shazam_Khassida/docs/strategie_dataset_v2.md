# Shazam Khassida - Stratégie de Constitution du Dataset V2

Ce document synthétise l'analyse du problème de "Démarrage à froid" (Cold Start) pour la V2, en s'appuyant sur les réflexions de l'utilisateur (`recherche/note_temp`) et les acquis de l'ancien projet de classification (`Classify_Khassida`).

## 1. Le Constat de Départ
*   **Rejet de l'ASR (Whisper) :** L'approche de transcription texte-à-texte est écartée. Les chants religieux sénégalais (mélange Wolof/Arabe, rythmique unique, accentuation locale forte) provoqueront trop d'hallucinations sur des modèles ASR formés sur de l'Arabe standard.
*   **La Mine d'Or brute :** Un canal Telegram a été identifié contenant environ **5000 fichiers audios**.
*   **Le Bloquant (Cold Start Problem) :** Les noms de ces 5000 fichiers sont chaotiques (ex: `AUDIO-2023-04-12-WA0012_mame_mor_touba_khassida_jasbul_qulub_live.mp3`). Il est impossible d'entraîner une IA V2 sans étiqueter ces 5000 fichiers, et il est humainement impossible de tous les écouter.

## 2. L'Héritage du projet `Classify_Khassida`
L'analyse de l'ancien projet `Classify_Khassida` révèle que la moitié du travail pour résoudre ce problème a **déjà été faite** !
*   Les scripts `extract_khassida_titles.py` et `process_csv.py` ont permis d'extraire des centaines de titres depuis des fichiers HTML et CSV.
*   Surtout, **`normalize_titles.py`** a fait un travail remarquable de *Nettoyage et Clustering Textuel* (suppression d'accents, minuscules, `difflib.SequenceMatcher`) pour regrouper les variations orthographiques (ex: *Bouchera-Lana* vs *Buchra lanâ*).
*   **Le Résultat :** Ce projet a généré une **Liste Canonique de Référence** des noms de Khassidas vrais et validés.

## 3. Le Plan d'Action (Pipeline de Labellisation Automatisée)

Pour transformer les 5000 audios chaotiques en un Dataset V2 propre et étiqueté, nous allons fusionner les 3 solutions théoriques en un seul Pipeline pragmatique :

### Étape 1 : Le "Fuzzy Matching" sur les Métadonnées (Gros du travail)
On recycle la logique de `Classify_Khassida`.
1. On liste les 5000 noms de fichiers Telegram.
2. On passe un coup de `normalize_text()` sur chaque nom de fichier pour enlever la casse, les tirets, et les accents.
3. On utilise `difflib.SequenceMatcher` pour comparer le nom du fichier nettoyé avec la **Liste Canonique de Référence** issue de ton ancien projet.
*Résultat attendu : 60% à 70% des fichiers seront automatiquement et formellement identifiés juste par leur titre.*

### Étape 2 : L'Extraction Intelligente par LLM (Pour les cas difficiles)
Pour les 30% restants dont le titre contient des mots, mais trop bruités pour un Fuzzy Matcher (ex: `Enregistrement_Wa_Kourel_Touba_J_Qulub.mp3`).
1. On envoie ces noms de fichiers à un petit LLM (ex: `gpt-4o-mini` ou un modèle local via Ollama).
2. On lui donne le prompt : *"Voici une liste de 500 noms de Khassidas officiels. À quel Khassida ce nom de fichier corrompu fait-il référence ?"*
*Résultat attendu : Résolution de 20% supplémentaires.*

### Étape 3 : Le Clustering Audio Non-Supervisé (Pour les fichiers "Aveugles")
Pour les 10% restants dont le nom ne veut absolument **rien dire** (ex: `AUDIO-2023-04-12-WA0012.mp3`) ou dont l'étiquetage texte a échoué.
1. On n'écoute pas l'audio ! On le fait passer dans un modèle audio générique (Wav2Vec 2.0 ou VGGish) pour le transformer en un vecteur mathématique.
2. On utilise UMAP + HDBSCAN pour regrouper ces audios par "Similarité acoustique".
3. L'algorithme va dire : *"Les fichiers aveugles X, Y et Z se ressemblent à 99%."*
4. **Action Manuelle (Active Learning) :** Tu n'écoutes que **1 seul fichier** (le X). Tu réalises que c'est *Midadi*. Tu viens de labelliser magiquement Y et Z en même temps.

## 4. Prochaine Étape Recommandée
Avant de coder le moindre réseau de neurones pour la *reconnaissance Shazam* (V2), le projet immédiat est de coder ce **Pipeline de Labellisation Automatisée** (Data Engineering).

Souhaites-tu que l'on commence par écrire un script qui scanne le dossier de tes 5000 fichiers audios Telegram, et qui tente l'Étape 1 (Fuzzy Matching contre ton dictionnaire `Classify_Khassida`) pour voir quel pourcentage de ton Dataset on arrive à classifier "gratuitement" ?
