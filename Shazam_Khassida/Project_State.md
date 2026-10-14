# État du Projet : WakhMu (Shazam Khassida)

## 🎯 Objectif Principal
Créer une application mobile et web permettant de reconnaître instantanément un Khassida à partir d'un extrait audio (type Shazam), avec une bibliothèque complète pour lire et écouter les œuvres (Kàggu).

## 📊 État d'avancement Global
- **Frontend** : 🟢 Terminé (Mock-driven)
- **Dataset / Backend** : 🔴 À faire
- **Reconnaissance IA** : 🔴 À faire
- **Déploiement Mobile** : 🟡 En attente de finalisation (Capacitor)

## 📋 Tâches en cours / À faire

### Phase 1 : Frontend & UI (✅ Terminée)
- [x] Initialisation projet React + Vite + Zustand + Dexie
- [x] Implémentation du Design System (inspiré de "Innovation Mouride")
- [x] Page Accueil (Bouton Shazam, historique récent)
- [x] Page Kàggu (Bibliothèque Khassida & Khassida PDF)
- [x] Lecteur Khassida (Texte arabe Amiri, translittération, Audio Player mocké)
- [x] Simulation de l'IA (`mockAI.js`)
- [x] Document de sécurité rédigé : [[docs/SECURITE.md]]

### Phase 2 : Le Cœur de l'Application (En cours)
- [ ] Mettre en place la stratégie pour la constitution du Dataset (voir [[docs/strategie_dataset_v2.md]])
- [ ] Développer le modèle de reconnaissance audio
- [ ] Remplacer le `mockAI` par de véritables appels API
- [ ] Remplir le catalogue de Khassidas avec de véritables données textuelles et les audios de référence

### Phase 3 : Finalisation & Mobile
- [ ] Vérification globale de la sécurité (voir [[docs/SECURITE.md]])
- [ ] Intégration de Capacitor pour build l'APK Android
- [ ] Gestion des permissions natives (Microphone)

## 🔗 Liens Rapides
- Architecture Technique et Stack : [[docs/TECH_STACK.md]]
- Directives et règles de dev : [[Rules]]
- Journal d'évolution et apprentissages : [[Journal_Evolution]]
