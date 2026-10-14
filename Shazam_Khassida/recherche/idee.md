
# 🎯 OBJECTIF DU PROTOTYPE

Identifier automatiquement **quelle Khassida** est chantée à partir d’un extrait audio, en gérant :

* plusieurs versions par Khassida
* variations légères de tempo / voix
* bruit modéré

Sans transcription.
Sans ML complexe.
Sans réentraîner un modèle.

---

# 🧠 ARCHITECTURE GÉNÉRALE

Ton système aura **4 blocs** :

```
1. Base audio (multi-version)
2. Générateur de fingerprints
3. Base de fingerprints indexée
4. Moteur de matching + score probabiliste
```

---

# 🏗️ STRUCTURE DU PROJET

Voici la structure minimale recommandée :

```
khassida_shazam/
│
├── data/
│   ├── raw/
│   │   ├── khassida_1/
│   │   │   ├── version1.wav
│   │   │   ├── version2.wav
│   │   │
│   │   ├── khassida_2/
│   │   │   ├── version1.wav
│   │   │
│
├── fingerprints_db/
│   ├── index.pkl   (ou sqlite)
│
├── build_db.py
├── match.py
├── preprocess.py
└── config.yaml
```

---

# ⚙️ ÉTAPE 1 — CHOIX DU REPO SHAZAM-LIKE

Tu ne veux pas recoder le moteur. Très bien.

Cherche un repo avec :

* génération de spectrogramme
* extraction de peaks
* hash pairing (Shazam-style)
* matching basé sur offset alignment

Tu veux quelque chose qui fait :

```
Audio → Spectrogram → Peak pairs → Hashes → Database
```

C’est la structure classique Shazam.

Ton agent IA peut :

* fork un repo Python Shazam-like
* supprimer la partie UI
* garder uniquement :

  * fingerprint generation
  * database storage
  * match scoring

---

# ⚙️ ÉTAPE 2 — BUILD DATABASE

Script : `build_db.py`

Ce qu’il fait :

1. Parcourt `data/raw/`
2. Pour chaque version :

   * normalise (mono, 16kHz)
   * génère les fingerprints
3. Stocke dans une base indexée :

Structure recommandée :

```
{
  hash_value: [
      (khassida_id, version_id, offset_time),
      ...
  ]
}
```

⚠️ IMPORTANT :
Le hash ne contient PAS le son entier.
Seulement des signatures locales robustes.

---

# ⚙️ ÉTAPE 3 — MATCHING

Script : `match.py`

Processus :

1. L’utilisateur fournit un extrait audio (5-10 secondes)
2. Génération des fingerprints
3. Recherche des hashes correspondants
4. Calcul d’un score :

### Méthode probabiliste simple

Pour chaque Khassida :

```
score = nombre_de_hash_matchés / nombre_total_hash_extrait
```

Ou mieux :

* compter les alignements cohérents en temps
* garder la Khassida avec le pic d’offset dominant

👉 C’est ce que fait Shazam :
il cherche un alignement temporel dominant.

---

# 🧪 CE QUE TU DOIS TESTER (IMPORTANT)

### Phase 1 — Validation minimale

* 2 Khassidas
* 1 version chacune
* test avec extrait exact

Tu dois obtenir :
✔️ reconnaissance parfaite

---

### Phase 2 — Robustesse version

* Ajouter 2 versions supplémentaires
* Tester :

  * extrait de version différente
  * bruit léger
  * tempo légèrement modifié

Tu dois obtenir :
✔️ score élevé pour la bonne Khassida
✔️ score faible pour l’autre

---

### Phase 3 — Tolérance

Tester :

* enregistrement micro
* compression mp3
* bruit de fond léger

Tu observes :

* à partir de quel seuil ça casse
* ajustement taille fenêtre / seuil peak

---

# 🔬 PARAMÈTRES CRITIQUES À COMPRENDRE

Ton agent IA devra te laisser contrôler :

| Paramètre                       | Impact                     |
| ------------------------------- | -------------------------- |
| taille fenêtre FFT              | résolution fréquence       |
| seuil détection peak            | bruit vs robustesse        |
| nombre de peaks par segment     | précision                  |
| distance max entre peaks pairés | robustesse variation tempo |

Tu ne modifies pas l’algo,
tu ajustes ces hyperparamètres.

---

# 🧠 LOGIQUE MULTI-VERSION

Très important.

Quand tu matches :

Tu ne choisis PAS la version.

Tu fais :

```
Score par version
→ Agrégation par Khassida
→ Max ou moyenne
```

Donc :

Khassida_1 = max(score_version1, score_version2, score_version3)

Ça permet :
✔️ robustesse naturelle
✔️ gestion variations

---

# 📈 CE QUE TU DOIS COMPRENDRE À LA FIN

Si ton prototype marche, tu dois pouvoir expliquer :

1. Pourquoi deux versions différentes matchent
2. Pourquoi un bruit léger ne casse pas tout
3. Pourquoi un chant totalement différent ne match pas
4. Pourquoi l’alignement temporel est la clé

Si tu comprends ça,
tu maîtrises 80% du système.

---

# 🚀 RÉALITÉ DU PROTOTYPE

Oui, c’est raisonnable.

Avec :

* 2 Khassidas
* 3 versions chacune
* 5–10 secondes d’extrait

Tu peux avoir un prototype fonctionnel en quelques jours.

---

# 🔥 CE QUE TU NE DOIS PAS FAIRE

❌ Ne pas commencer par l’annotation texte
❌ Ne pas essayer d’améliorer l’IA au début
❌ Ne pas entraîner un modèle deep learning

Tu construis :
**un moteur déterministe robuste**

---------------------------------------------------

Tu as mis dans le mille. Ton analyse est chirurgicale et tu as identifié exactement les limites théoriques et pratiques de l'approche par DTW. C'est précisément pour ces raisons (lenteur $O(N \times M)$ et sensibilité au bruit) que l'algorithme de Shazam a révolutionné l'industrie pour la reconnaissance d'enregistrements *exacts*.

Tu as soulevé les vrais défis d'ingénierie d'un système audio. Voici comment nous pouvons parer ces problèmes un par un pour construire un prototype qui tient la route, sans pour autant basculer dans une usine à gaz.

---

### 🛡️ Réponses aux failles identifiées et Solutions

**A. La Lenteur du DTW ($O(N \times M)$)**
Tu as totalement raison, comparer 15s contre 5 minutes va faire exploser le CPU.

* **La solution pour l'agent : Le "Chunking" (Segmentation).** Au lieu de stocker le Khassida entier comme une seule matrice, le script `build_db.py` doit découper l'audio de référence en segments de 15 secondes (avec un chevauchement de 5 secondes). Ainsi, le DTW ne compare que des matrices de taille similaire ($15s \times 15s$). C'est massivement plus rapide.
* **Alternative :** Utiliser l'implémentation `fastdtw` (disponible en Python) qui réduit la complexité temporelle et spatiale à $O(N)$.

**B. La Répétitivité et la faible harmonie (Limites du Chromagramme)**
C'est une excellente remarque. Les Khassidas étant essentiellement vocales (parfois monocordes), la signature harmonique (Chroma) risque d'être trop "plate".

* **La solution pour l'agent : Passer aux MFCC (Mel-Frequency Cepstral Coefficients).** Les MFCC sont la norme absolue pour la reconnaissance vocale et le traitement de la parole. Ils capturent le "timbre" de la voix et l'articulation (les phonèmes) plutôt que la note de musique brute. Demande à l'agent d'utiliser `librosa.feature.mfcc()` au lieu de `chroma_cqt()`.

**C. La sensibilité au bruit et à la réverbération**
Le DTW cherchera à aligner le bruit de fond s'il est trop présent.

* **La solution pour l'agent : Le filtrage HPSS (Harmonic-Percussive Source Separation).** C'est une fonction magique de `librosa` (`librosa.effects.hpss()`) qui sépare la voix (harmonique) des bruits secs/clics (percussifs) avant même de calculer les features. Cela nettoie énormément le signal.

**D. Le manque de Scalabilité (Scalability)**
C'est le mur classique du passage en production.

* **La réalité du prototype :** Pour ton prototype (2 Khassidas, 3 versions, découpées en chunks), une boucle for sera calculée en moins d'une seconde.
* **La vision future :** Quand tu passeras à 500 Khassidas, tu ne feras plus de DTW brutal. Tu utiliseras une base vectorielle comme **FAISS** (de Meta) pour faire un pré-filtrage instantané (trouver les 5 chunks les plus proches), et tu n'appliqueras le DTW *que* sur ces 5 candidats pour affiner. Mais ce n'est pas le but de la Phase 1.

---

### 🧬 L'Architecture Hybride (La meilleure approche)

Si tu veux vraiment couvrir tous les cas d'usage (enregistrements exacts bruités + variations de chant), la norme industrielle est l'architecture à deux étages ("Two-Pass Search").

1. **Pass 1 (Ultra-rapide) - Le Fingerprinting (Shazam) :** On cherche une correspondance de hash exacte. Si on trouve (score élevé), c'est gagné, on s'arrête là (temps de réponse : 0.1s). Gère parfaitement le bruit fort et la mosquée.
2. **Pass 2 (Profond) - Le DTW sur MFCC :** Si le Pass 1 échoue (score faible), cela signifie que l'utilisateur chante lui-même ou que c'est une version non répertoriée. On lance l'alignement DTW sur les chunks MFCC pour trouver la similarité vocale.

# Point a surveillé

❗ A. HPSS (Harmonic/Percussive Separation)

librosa.effects.hpss fonctionne bien sur musique.

Mais sur voix a cappella :

La voix est déjà harmonique

Le bruit ambiant peut être mal classé

Ça peut :

Aider

Ou parfois dégrader légèrement

Ce n’est pas mauvais, mais il faudra tester.

❗ B. MFCC + DTW peut confondre des Khassidas proches

Si deux Khassidas :

ont un même mode mélodique

sont récitées sur la même base

Les MFCC peuvent être trop proches.

Ce n’est pas une erreur d’architecture.
C’est une limite structurelle du signal.

❗ C. Seuils de décision

Tu vas devoir calibrer :

seuil_confiance fingerprint

seuil_tolerance DTW

Et ça demande :

dataset test varié

vraie phase d’évaluation

Mais c’est normal
-----------------------

de mon experience et du recul que j'ai, je sais que cette methode avec whisper ne sera pas efficace sur les khassidas. Il faut plutot sur la resolution du probleme : un constat, peu importe là où je prends mes audios (youtube+conversion, audio from telegram ou autre sites par scrapping...) le titre des audios est bien bordélique. Cela fait echo avec l'un de mes anciens projet que j'ai laissé tomber faute de temps qui consiter justement au classement d'audio de khassida juste à partir de leurs audios... Bref il faudrait trouver une solution efficace pour ce probleme.  
-----------------

Tu as un excellent instinct. L'approche Whisper (ASR) sur des chants religieux sénégalais (mélange d'arabe, de wolof, avec une rythmique et une accentuation vocale uniques) a en effet toutes les chances de produire des hallucinations ou des transcriptions inexploitables.

Tu mets le doigt sur le vrai problème, le "mur" classique en Data Science : **Le problème du démarrage à froid (Cold Start Problem).** Tu as 5000 fichiers, mais leurs noms sont inutilisables. Tu ne peux pas entraîner d'IA sans données étiquetées, mais tu ne peux pas étiqueter 5000 fichiers à la main. C'est exactement le problème de ton ancien projet de classement.

Puisque nous écartons l'approche algorithmique pure (qui échoue sur les variations) et l'approche Whisper, voici **3 solutions pragmatiques et modernes** pour résoudre ce chaos et construire ton dataset proprement.

---

### Solution 1 : Le Clustering Audio Non-Supervisé (La revanche de ton ancien projet)

Puisque ton idée était de classer les Khassidas *uniquement à partir de l'audio*, c'est aujourd'hui tout à fait possible sans avoir à entraîner un modèle de zéro.

* **Le principe :** On ne demande pas à l'IA de *reconnaître* le Khassida, on lui demande juste de regrouper les fichiers qui se ressemblent mathématiquement.
* **Comment faire ?**

1. On fait passer tes 5000 audios dans un modèle pré-entraîné généraliste (comme **VGGish** de Google ou **Wav2Vec 2.0**). Ces modèles transforment chaque audio en un "Vecteur" (Embedding).
2. On utilise des algorithmes de réduction de dimension (UMAP) et de clustering (HDBSCAN).
3. L'algorithme va créer des "grappes" (clusters).

* **L'avantage massif :** Tu vas te retrouver avec, par exemple, le Cluster N°12 contenant 150 audios. Tu en écoutes *un seul*. Tu réalises que c'est *Midadi*. Boom : tu viens d'étiqueter 150 fichiers d'un seul coup en 5 secondes.

### Solution 2 : Le Nettoyage NLP par LLM (Extraction de Métadonnées)

Même si un titre Telegram est "bordélique" (ex: `AUDIO-2023-04-12-WA0012_mame_mor_touba_khassida_jasbul_qulub_live.mp3`), il contient souvent des pépites d'information. Les expressions régulières (Regex) classiques vont s'y casser les dents, mais pas un LLM léger.

* **Le principe :** Utiliser un modèle de traitement du langage naturel pour "lire" les noms de fichiers bizarres et en extraire l'intention.
* **Comment faire ?**

1. Tu listes les 5000 noms de fichiers dans un fichier texte.
2. Tu fournis à un LLM (via API ou en local) la liste des 50 vrais noms de Khassidas que tu cibles.
3. Tu lui demandes : *"Pour chaque nom de fichier corrompu, trouve à quel Khassida officiel il correspond le plus, ou renvoie 'Inconnu'"*.

* **Le résultat :** Tu obtiens un fichier CSV propre avec un étiquetage probabiliste. Tu n'auras plus qu'à vérifier manuellement ceux marqués comme "Inconnu".

### Solution 3 : L'Apprentissage Actif (Active Learning)

C'est la méthode hybride la plus utilisée en industrie pour créer des datasets rapidement.

* **Le principe :** Tu travailles main dans la main avec un petit modèle d'IA.
* **Comment faire ?**

1. Tu écoutes et tu étiquettes manuellement seulement **50 fichiers** (ex: 10 *Midadi*, 10 *Sindidi*, etc.).
2. Tu entraînes un petit réseau de neurones (Approche A) uniquement sur ces 50 fichiers.
3. Tu demandes au modèle de prédire les 4950 fichiers restants.
4. Le modèle va te donner un score de confiance. Tu acceptes automatiquement tout ce qui est >95% de confiance.
5. Tu n'écoutes manuellement que les fichiers où le modèle a douté (ex: 50% de confiance), tu les corriges, et tu réentraînes.

* **L'avantage :** Le modèle devient ton assistant de tri. Plus tu corriges, moins tu as de travail.

---

### Mon avis sur la marche à suivre

Si j'étais à ta place, je combinerais **la Solution 2 (pour dégrossir immédiatement grâce aux titres)** et **la Solution 1 (Clustering sur les fichiers restants mal nommés)**.
