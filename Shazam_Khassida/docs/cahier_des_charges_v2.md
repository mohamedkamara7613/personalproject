# Shazam Khassida - Cahier des Charges & Spécifications V2

Ce document définit les objectifs, les besoins en données (Dataset) et les pistes algorithmiques pour la prochaine itération du projet de reconnaissance vocale de Khassidas de Serigne Touba.

## 1. Objectif Principal

Développer un moteur capable d'écouter un enregistrement audio (via microphone mobile, avec bruits de rue/foule) de 10 à 20 secondes, et de déterminer avec un haut degré de certitude le **texte originel (Khassida)** récité, et ce :

* Indépendamment du lecteur (voix grave, aiguë, enfant, chœur).
* Indépendamment de la vitesse ou du rythme (lent, saccadé, ornementé).
* Avec une tolérance élevée à la compression audio des messageries (WhatsApp vocal).

## 2. Le Besoin Critique : Constitution d'un Dataset

La méthode algorithmique pure de la V1 a échoué car elle manquait de "contexte". L'Intelligence Artificielle moderne a besoin d'apprendre la "variance" d'un chant. Nous ne pouvons pas démarrer la V2 sans un Dataset solide.

### 2.1 Critères du Dataset idéal

Pour entraîner un modèle de Machine Learning ou valider un système robuste, il nous faut une collection d'audios répondant aux critères suivants :

* **Volume :** Au moins 50 Khassidas différents.
* **Variété (Multi-locuteurs) :** Pour chaque Khassida, il faut **plusieurs versions** chantées par **différentes personnes** (ex: Serigne Mame Mor, Sokhna Mai, des talibés anonymes).
* **Réalité du terrain :** Des qualités d'enregistrement disparates (studio, live de Magal, enregistrement téléphone).
* **Annotation stricte :** Chaque fichier doit être formellement étiqueté (`ID_Khassida_Verité`). s

### 2.2 Comment se procurer ce Dataset ?

* **Recherche de Datasets Existants :** Il faut explorer les plateformes académiques (Kaggle, HuggingFace) ou les archives universitaires sénégalaises. Existe-t-il déjà un corpus d'audios wolof/arabes religieux annoté ? (Probabilité faible).
* **Scraping (Collecte Automatisée) :** Extraire le catalogue audio de plateformes comme *MourideTube*, *Dahira*, ou des chaînes YouTube dédiées. L'extraction du titre de la vidéo servirait d'annotation automatique.
* **Crowdsourcing (Participatif) :** Créer une application web basique demandant aux disciples d'enregistrer 15 secondes d'un Khassida précis depuis leur téléphone pour alimenter la base de recherche.
* **Partenariats :** Contacter les radios ou médiathèques mourides qui disposent déjà d'archives cataloguées numériquement.

## 3. Approches Technologiques pour la V2

Une fois le Dataset acquis, le développement pourra s'orienter vers l'une de ces 3 voies majeures :

### Approche A : Embeddings Vocaux (Réseaux Siamois / Contrastive Learning)

* **Principe :** On entraîne un Réseau de Neurones Profond (Deep Neural Network) à écouter un Mel-Spectrogramme et à le compresser en un "Vecteur de 512 nombres" (un Embedding). Le réseau est forcé de comprendre que "La voix de A chantant Midadi" = "La voix de B chantant Midadi", et va rapprocher leurs vecteurs mathématiquement, tout en éloignant le vecteur de "C chantant Rabibima".
* **Mise en œuvre :** Utilisation de PyTorch. Adaptation d'architectures spécialisées en audio (ResNet34, Wav2Vec 2.0).
* **Avantages :** Extrêmement robuste aux variations vocales. C'est l'état de l'art actuel.

### Approche B : Reconnaissance Vocale (ASR) + Recherche Textuelle Polyglotte

* **Principe :** Au lieu de comparer du son avec du son, on utilise l'Intelligence Artificielle pour **transcrire** l'audio en texte arabe/wolof (Speech-To-Text), même approximativement. On compare ensuite le texte obtenu à une base de données de Khassidas PDF via des algorithmes de NLP (Recherche Floue, Levenshtein, ElasticSearch).
* **Mise en œuvre :** Utilisation du modèle *Whisper* d'OpenAI (qui supporte l'Arabe et excelle en milieu bruité) ou fine-tuning d'un modèle ASR sur des chants islamiques sénégalais.
* **Avantages :** Résout totalement le problème de rythme et du chanteur. Si les paroles sont reconnues, le Khassida est identifié.

### Approche C : Fingerprinting Temporel Avancé (Moteur robuste au "Pitch/Tempo")

* **Principe :** Une version très évoluée du Pass 1 de notre V1. Au lieu de regarder des pics temporels exacts, l'algorithme génère des empreintes géométriques tolérantes aux étirements (ex: Algorithme *Panako* qui résiste aux changements de tempo de +/- 20% et aux transpositions de tonalité).
* **Mise en œuvre :** Recherche académique sur les "Robust Audio Fingerprints" et implémentation en C++ ou Python fortement optimisé.
* **Avantages :** Pas besoin d'entraîner l'IA sur des jours entiers. Rapide et peu gourmand en ressources, à condition d'avoir LA référence originelle qui s'en rapproche le plus.

## 4. Recommandations pour l'Avancement

1. Geler le code de la V1 et l'archiver pour référence mathématique.
2. Débuter la **Phase d'Investigation Dataset** : chercher s'il existe une base de 100 à 1000 heures de Khassidas qualifiés.
3. Évaluer la faisabilité de l'**Approche B (ASR Whisper)** sur un extrait chanté pour observer si la transcription textuelle de l'Arabe (avec l'accentuation typique) est exploitable avant de s'engager sur un lourd modèle acoustique.

---
Voici la transcription structurée et propre de tout ce que tu as expliqué sur ton projet.

---

Transcription – Projet Shazam Khassida

1. Présentation du projet

Le projet que je souhaite réaliser s'appelle Shazam Khassida.
Ce n'est pas exactement le même type de projet que l'application Shazam classique, mais le principe est similaire.

Les Khassidas sont des chants religieux de Serigne Touba.
Ils sont souvent récités ou chantés, parfois a cappella, et ils ressemblent dans leur forme à la récitation coranique.

L'objectif du projet est de créer un moteur capable d'identifier un Khassida à partir d'un enregistrement audio.

Cet enregistrement peut être :

une personne seule qui chante le Khassida (a cappella)

un groupe de personnes qui récitent le Khassida

un extrait court de la récitation

À partir de cet enregistrement, le système devra être capable de déterminer de quel Khassida il s'agit.

---

1. Comparaison avec des applications existantes

Le projet ressemble à deux types d'applications existantes :

1. Shazam

Shazam permet, à partir d'un extrait d'une chanson, de retrouver la chanson correspondante.

1. Tartil (application Android)

Tartil permet de reconnaître quel verset du Coran est en train d'être récité.

Le projet Shazam Khassida serait donc une application similaire, mais appliquée aux Khassidas.

---

1. Problème principal du projet

Le principal problème vient du fait que les Khassidas sont des poèmes.

Cela implique que :

Un même Khassida peut être chanté dans plusieurs styles différents.

Par exemple :

Khassida A peut être chanté :

dans un style 1

dans un style 2

Mais le problème est plus complexe :

Un autre Khassida, écrit avec le même rythme poétique, peut aussi être chanté :

dans le style 1

dans le style 2

Donc deux Khassidas différents peuvent être chantés avec exactement le même style musical.

Cela signifie que :

> Il ne faut pas confondre deux Khassidas simplement parce qu'ils sont chantés dans le même style.

C'est probablement le principal défi du projet de reconnaissance.

---

1. Problème du dataset

Pour développer ce projet, il faut un dataset audio de Khassidas.

Ce dataset serait nécessaire pour :

entraîner le modèle

tester les algorithmes

optimiser la reconnaissance

Mais pour l'instant :

ce domaine semble très peu documenté

il est difficile de trouver un dataset existant

Donc plusieurs questions se posent :

Où trouver un dataset de Khassidas ?

Est-ce qu'il existe déjà quelque part ?

Faut-il faire du scraping pour récupérer les données ?

Quels outils modernes permettent de faire ce scraping ?

Une autre question importante est :

> Est-ce que je dois créer moi-même ce dataset ?

Si c'est le cas, cela deviendrait un projet à part entière :

collecter les enregistrements

les nettoyer

les annoter

les structurer

---

1. Questions techniques sur la méthode

Une fois les données disponibles, il faut déterminer comment construire le moteur de reconnaissance.

Plusieurs approches sont possibles :

1. Reconnaissance vocale

Utiliser des techniques de speech recognition pour analyser la récitation.

1. Traitement du signal audio

Utiliser des méthodes de signal processing pour extraire les caractéristiques audio.

1. Intelligence artificielle

Utiliser un modèle d'IA et éventuellement :

le fine-tuner

l'entraîner spécifiquement pour la reconnaissance des Khassidas.

---

1. Question fondamentale

Une question centrale reste :

> Est-ce qu'il est réellement nécessaire de créer un dataset soi-même ?

Ou bien existe-t-il déjà :

des datasets

des archives

des bases de données audio

qui pourraient être utilisées.

---

Résumé du projet

Le projet consiste à développer un système similaire à Shazam capable :

d'écouter un extrait audio d'un Khassida

et d'identifier automatiquement le Khassida correspondant

Les défis principaux sont :

1. La variabilité des styles de chant

2. La confusion possible entre Khassidas ayant le même rythme

3. L'absence apparente de dataset existant

4. Le choix de la méthode technique la plus adaptée

---
