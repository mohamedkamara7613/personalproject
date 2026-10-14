# Stack Technique — LifeCal
## Guide pour reproduire une app similaire

> Ce document explique chaque technologie utilisée dans LifeCal, pourquoi elle a été choisie, et comment les pièces s'assemblent. Il est rédigé pour servir de référence lors de la création d'une application du même type.

---

## Vue d'ensemble de l'architecture

```
┌─────────────────────────────────────────────────┐
│                    ANDROID APK                  │
│  ┌───────────────────────────────────────────┐  │
│  │           Capacitor (bridge)              │  │
│  │  ┌─────────────────────────────────────┐ │  │
│  │  │        WebView Android              │ │  │
│  │  │  ┌──────────────────────────────┐  │ │  │
│  │  │  │   React + Vite (web app)     │  │ │  │
│  │  │  │   ├── Zustand (état global)  │  │ │  │
│  │  │  │   └── Dexie.js (IndexedDB)   │  │ │  │
│  │  │  └──────────────────────────────┘  │ │  │
│  │  └─────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

Les données ne quittent jamais l'appareil. Tout est stocké localement dans IndexedDB.

---

## 1. Vite — Le bundler

**Rôle** : compile et optimise le code JavaScript/React pour la production.

**Pourquoi Vite ?**
- Démarrage quasi-instantané en développement (Hot Module Replacement)
- Build ultra-rapide (~200ms pour LifeCal)
- Compatible nativement avec React et les modules ES

**Configuration clé pour Capacitor** :
```js
// vite.config.js
export default defineConfig({
  plugins: [react()],
  base: './',  // ← OBLIGATOIRE pour Capacitor (chemins relatifs dans le WebView)
})
```

**Commandes** :
```bash
npm run dev        # Serveur local (http://localhost:5173)
npm run build      # Génère le dossier dist/ (fichiers statiques)
npm run preview    # Prévisualise le build de production
```

---

## 2. React — Le framework UI

**Rôle** : construit l'interface utilisateur de façon déclarative avec des composants réutilisables.

**Pourquoi React ?**
- Écosystème mature, nombreux exemples et bibliothèques
- Composants = blocs réutilisables (Navbar, CapsuleModal, AudioRecorder…)
- Hooks (`useState`, `useEffect`, `useRef`) pour la logique locale

**Structure du projet** :
```
src/
├── pages/          ← Pages complètes (Dashboard, LifeRug, Stats, Settings)
├── components/     ← Composants réutilisables (Navbar, CapsuleModal, AudioRecorder)
├── hooks/          ← Logique réutilisable (useSwipeNavigation)
├── store/          ← État global (Zustand)
├── engine/         ← Calculs purs (calendar.js)
├── db/             ← Base de données (lifecal.db.js)
└── index.css       ← Design system complet
```

---

## 3. Zustand — L'état global

**Rôle** : partage les données entre composants sans passer des props partout.

**Pourquoi Zustand ?**
- API simple (3 lignes pour créer un store)
- Pas de boilerplate comme Redux
- Persistance facile avec `zustand/middleware`

**Exemple de store** :
```js
import { create } from 'zustand';

const useStore = create((set) => ({
  activePage: 'dashboard',
  navigate: (page) => set({ activePage: page }),

  theme: 'dark',
  toggleTheme: () => set((s) => ({ theme: s.theme === 'dark' ? 'light' : 'dark' })),
}));
```

**Données gérées dans LifeCal** :
- Profil utilisateur (date de naissance, snapshot de la semaine)
- Navigation (page active)
- Thème (dark/light)
- État du modal de capsule

---

## 4. Dexie.js — La base de données locale

**Rôle** : stocke toutes les données (capsules, photos, audios) dans le navigateur via IndexedDB.

**Pourquoi Dexie ?**
- IndexedDB natif est complexe à utiliser, Dexie simplifie tout
- Supporte les requêtes, index, transactions
- Fonctionne dans le WebView Android de Capacitor

**Schéma de la base** :
```js
import Dexie from 'dexie';

const db = new Dexie('LifeCalDB');
db.version(1).stores({
  capsules: '++id, absoluteWeek, createdAt, mood, eventType',
  photos:   '++id, capsuleId, createdAt',
  audios:   '++id, capsuleId, createdAt',
  settings: 'key',
  badges:   '++id, type, unlockedAt',
});
```

**Avantage clé** : les données ne quittent jamais l'appareil. Pas de serveur, pas de compte, pas de cloud.

---

## 5. CSS Natif + Variables CSS — Le design system

**Rôle** : styles de toute l'application, avec système de thèmes.

**Pourquoi CSS natif (pas Tailwind) ?**
- Contrôle total sur les animations et effets complexes
- Les variables CSS permettent le changement de thème sans JavaScript
- Taille de bundle plus petite

**Système de variables** :
```css
/* Thème dark (défaut) */
[data-theme='dark'] {
  --bg-base:    #0a0a0f;
  --accent:     #8b5cf6;
  --text-primary: #f1f0ff;
  /* ... */
}

/* Thème light */
[data-theme='light'] {
  --bg-base:    #f8f7ff;
  --accent:     #7c3aed;
  --text-primary: #1a1030;
  /* ... */
}
```

Pour changer de thème : `document.documentElement.setAttribute('data-theme', 'light')`.

---

## 6. Capacitor — Le bridge web → Android

**Rôle** : transforme l'application web en APK Android installable, avec accès aux fonctions natives.

**Pourquoi Capacitor ?**
- Zéro réécriture : le même code React tourne dans un WebView
- Accès aux API natives (micro, caméra, notifications, vibration…)
- Génère un projet Android Studio standard
- Concurrent direct : Cordova (plus ancien), React Native (réécriture complète)

**Comment ça marche** :
```
Code React → build Vite (dist/) → copié dans android/app/src/main/assets/
Capacitor WebView charge index.html depuis les assets locaux
Les plugins JS appellent du code Java natif via un bridge
```

**Plugins utilisés dans LifeCal** :
| Plugin | Rôle |
|--------|------|
| `@capacitor/app` | Bouton retour Android, minimiser l'app |
| `@capacitor/status-bar` | Couleur et transparence de la barre de statut |
| `@capacitor/local-notifications` | Notifications quotidiennes planifiées |

**Workflow** :
```bash
npm install @capacitor/core @capacitor/cli
npx cap init "NomApp" "com.nomapp.id" --web-dir dist
npm install @capacitor/android
npx cap add android
npm run build && npx cap sync android
# Puis ouvrir Android Studio ou utiliser le script deploy.sh
```

---

## 7. MediaRecorder API — L'enregistrement audio

**Rôle** : enregistre l'audio du microphone directement dans le navigateur/WebView.

**Pas besoin de plugin externe !** C'est une API web standard.

```js
const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
const recorder = new MediaRecorder(stream);
recorder.start();

recorder.ondataavailable = (e) => chunks.push(e.data);
recorder.onstop = () => {
  const blob = new Blob(chunks, { type: 'audio/webm' });
  // Stocker dans IndexedDB via Dexie
};
```

**Permission Android requise** dans `AndroidManifest.xml` :
```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
```

---

## 8. Web Speech API — La transcription vocale

**Rôle** : transcrit la parole en texte en temps réel, sans serveur.

**Pas de clé API, pas de cloud** (sur Android avec Chrome WebView).

```js
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
const recog = new SR();
recog.continuous = true;
recog.interimResults = true;  // résultats partiels en temps réel
recog.lang = 'fr-FR';         // ou 'en-US'
recog.start();

recog.onresult = (event) => {
  const transcript = Array.from(event.results)
    .map(r => r[0].transcript).join('');
};
```

⚠️ **Limite** : nécessite une connexion internet sur Android (Google traite la voix dans le cloud côté Android, pas côté JS). Sur desktop Chrome, ça peut fonctionner hors-ligne.

---

## 9. ADB — Le déploiement sans Play Store

**Rôle** : installe directement l'APK sur un téléphone Android connecté en USB.

```bash
# Vérifier les appareils connectés
adb devices

# Installer l'APK
adb install -r chemin/vers/app-debug.apk

# Voir les logs en temps réel
adb logcat | grep -i "chromium\|lifecal"
```

**Variable d'environnement à configurer** :
```bash
# Ajouter dans ~/.bashrc
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

---

## 10. Chrome DevTools Remote — Le debug sur appareil

**Rôle** : inspecter et débugger l'app sur le vrai téléphone depuis Chrome sur PC.

**Prérequis** :
1. `"webContentsDebuggingEnabled": true` dans `capacitor.config.json`
2. USB Debugging activé sur le téléphone
3. Téléphone branché en USB

**Utilisation** :
1. Ouvre Chrome → `chrome://inspect/#devices`
2. Ton téléphone apparaît → sous "LifeCal" clique **inspect**
3. DevTools complets : Elements, Console, Network, Sources avec sourcemaps

---

## Récapitulatif des dépendances

```json
{
  "dependencies": {
    "react": "^19",
    "react-dom": "^19",
    "zustand": "^5",
    "dexie": "^4",
    "@capacitor/core": "^8",
    "@capacitor/android": "^8",
    "@capacitor/app": "^8",
    "@capacitor/status-bar": "^8",
    "@capacitor/local-notifications": "^8"
  },
  "devDependencies": {
    "vite": "^8",
    "@vitejs/plugin-react": "^6"
  }
}
```

**Taille du bundle final** : ~350 KB JS (gzip: ~105 KB) — très léger pour une app complète.

---

## Checklist pour une nouvelle app similaire

```
[ ] npm create vite@latest mon-app -- --template react
[ ] cd mon-app && npm install
[ ] Configurer vite.config.js avec base: './'
[ ] npm install zustand dexie
[ ] Créer src/store/, src/db/, src/engine/
[ ] Écrire le design system dans index.css avec variables CSS
[ ] npm install @capacitor/core @capacitor/cli
[ ] npx cap init "MonApp" "com.monapp.id" --web-dir dist
[ ] npm install @capacitor/android
[ ] npx cap add android
[ ] Ajouter les permissions dans AndroidManifest.xml
[ ] npm run build && npx cap sync android
[ ] Ouvrir Android Studio → Build APK
[ ] adb install -r app-debug.apk
```

Les choix qu'on avait a faire :
Très bonne question. Il y a plusieurs technologies distinctes, chacune avec un niveau d'accès différent au téléphone. Voici une explication claire :

---

## Les 3 grandes familles

### 1. 🌐 PWA — Progressive Web App *(le plus simple, sans store)*

C'est exactement ce que tu décris : **une page web qui s'installe sur le téléphone**. Pas de Play Store, pas d'APK.

**Comment ça marche :**
- L'utilisateur ouvre l'URL dans Chrome sur Android
- Chrome propose "Ajouter à l'écran d'accueil"
- L'app se lance ensuite comme une vraie app (plein écran, sans barre d'adresse)

**Ce que ça donne accès :**
- ✅ Stockage local (IndexedDB) → **LifeCal le fait déjà**
- ✅ Mode hors-ligne (Service Worker)
- ✅ Notifications push
- ✅ Micro (pour l'audio)
- ✅ Caméra / photos
- ❌ Bluetooth, contacts, appels, NFC → **accès natif impossible**

> **LifeCal est déjà une PWA potentielle** — il suffit d'ajouter un `manifest.json` et un Service Worker.

---

### 2. 📦 Capacitor / Cordova *(le "intermédiaire" dont tu parles)*

C'est **exactement** l'intermédiaire que tu imagines. C'est ce que font Shein, Alibaba, et des milliers d'apps "hybrides".

**Comment ça marche :**
```
┌──────────────────────────────────────┐
│           Application Android        │
│  ┌────────────────────────────────┐  │
│  │        WebView (navigateur     │  │
│  │        intégré invisible)      │  │
│  │   ┌──────────────────────┐    │  │
│  │   │  Ton app React/HTML  │    │  │
│  │   └──────────┬───────────┘    │  │
│  │              │ appel JS       │  │
│  │   ┌──────────▼───────────┐    │  │
│  │   │   Bridge Capacitor   │◄───┼──┼── "Ouvre la caméra"
│  │   └──────────────────────┘    │  │   "Vibre le téléphone"
│  └────────────────────────────────┘  │   "Stocke un fichier"
│             Android natif            │
└──────────────────────────────────────┘
```

- **Capacitor** (fait par Ionic) est le successeur moderne de Cordova
- Ta page web React tourne dans un **WebView** (navigateur caché intégré dans l'APK)
- Le bridge JS ↔ Android permet d'appeler des fonctions natives : caméra, fichiers, Bluetooth, GPS précis, etc.
- Le résultat est un **fichier `.apk`** installable sans Play Store (sideload)

> C'est la technologie la plus adaptée à LifeCal si tu veux une vraie app Android avec accès au micro natif, notifications, etc.

---

### 3. ⚛️ React Native / Flutter *(apps vraiment natives)*

Là ce n'est **plus du tout une page web**. Le code est compilé en composants natifs Android réels.

| | PWA | Capacitor | React Native | Flutter |
|---|---|---|---|---|
| Pas de store | ✅ | ✅ (sideload APK) | ✅ (sideload APK) | ✅ |
| Ressemble à une web app | ✅ | ✅ | ❌ (natif) | ❌ (natif) |
| Accès micro/caméra | Partiel | ✅ complet | ✅ complet | ✅ complet |
| Effort depuis React | 0 | Faible | Réécriture | Réécriture |

---

## Pour LifeCal concrètement

Puisque c'est déjà une app React/Vite, **Capacitor** est la voie naturelle :

```bash
npm install @capacitor/core @capacitor/cli
npx cap init LifeCal com.lifecal.app
npx cap add android
npm run build     # génère le dossier dist/
npx cap sync      # copie dist/ dans l'APK
npx cap open android  # ouvre Android Studio
```

Ensuite depuis Android Studio tu génères l'APK → tu l'installes directement sur ton téléphone (sans Play Store, il faut juste activer "Sources inconnues" dans les paramètres Android).
