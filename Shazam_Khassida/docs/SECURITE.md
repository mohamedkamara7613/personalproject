# 🛡️ Sécurité & Bonnes Pratiques — WakhMu

Ce document liste les recommandations et pratiques de sécurité classiques à prendre en compte avant le lancement en production de l'application WakhMu (Shazam Khassida). L'architecture Frontend-First avec PWA + Capacitor requiert des considérations spécifiques.

---

## 1. Stockage Local (IndexedDB / LocalStorage)

Les données locales sont stockées via Dexie.js (IndexedDB). Bien qu'il n'y ait pas de données hautement sensibles (mots de passe, numéros de CB), l'historique de recherche représente des données personnelles d'utilisation.

- **Ne jamais stocker de tokens d'authentification en clair** dans IndexedDB ou LocalStorage. Utiliser les cookies `HttpOnly` ou le stockage sécurisé natif (si Capacitor : `@capacitor/preferences` + plugins de Secure Storage).
- **Injection IndexedDB** : Bien que rare, si des entrées utilisateur malveillantes sont insérées dans l'historique sans validation, cela peut corrompre la base locale. (Dexie protège contre la plupart des problèmes basiques, mais il faut s'assurer de toujours valider les données de retour de l'API).

## 2. Cross-Site Scripting (XSS)

Puisque React gère le rendu DOM, il nous protège nativement contre la plupart des attaques XSS classiques (échappement automatique des variables). Cependant, certaines failles restent possibles :

- **Ne jamais utiliser `dangerouslySetInnerHTML`** pour afficher le texte des Khassidas ou les traductions provenant d'une API externe, sans passer le contenu au préalable dans un "sanitizer" HTML (ex: `DOMPurify`).
- Attention aux URL des Khassida PDF et Audio récupérées depuis l'API. Toujours s'assurer qu'elles commencent par `https://` pour éviter l'exécution de JavaScript via des pseudo-protocoles (`javascript:...`).

## 3. Communications API & IA

Lorsque le mock sera remplacé par le véritable modèle d'intelligence artificielle :

- **HTTPS Forcé** : Tous les appels API (vers le serveur de reconnaissance ou les fichiers PDF/Audio) doivent obligatoirement utiliser HTTPS pour éviter les attaques de type Man-In-The-Middle (MITM).
- **Rate Limiting** : Protéger le serveur IA contre les attaques DDoS ou les abus de reconnaissance audio. L'API doit avoir une limite par IP/Token.
- **CORS (Cross-Origin Resource Sharing)** : Le serveur API doit restreindre les origines acceptées à celles de l'application WakhMu uniquement (l'URL PWA, et éventuellement `capacitor://localhost` ou `http://localhost`).

## 4. Permissions et Capacitor (Android)

L'application demandera potentiellement accès au microphone pour l'écoute :

- **Principe du moindre privilège** : Ne demander la permission du micro (`RECORD_AUDIO`) qu'au moment où l'utilisateur clique sur le bouton "Shazam" pour la première fois, avec une explication claire du pourquoi ("WakhMu a besoin du microphone pour écouter et identifier le Khassida").
- Vérifier que seules les permissions strictement nécessaires sont déclarées dans l'`AndroidManifest.xml`.
- Mettre à jour régulièrement les dépendances de `@capacitor/core` et `@capacitor/android` pour corriger les failles de sécurité des webviews.

## 5. Content Security Policy (CSP)

Pour la version web (PWA), configurer des en-têtes HTTP de sécurité au niveau du serveur (ou via une balise `<meta>` si strictement hébergé statiquement) :
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data: https:; media-src 'self' https:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;">
```
*Cette configuration empêche le chargement de scripts externes non autorisés.*

## 6. Protection contre l'ingénierie inverse (Reverse Engineering)

S'agissant d'un projet basé sur Capacitor/JS, le code source de l'APK (le bundle JS) est facilement extractible.
- Si le modèle IA ou des clés API sensibles doivent être protégés, la logique de reconnaissance **doit impérativement rester côté serveur** (Backend). L'application mobile (Frontend) ne doit envoyer que l'extrait audio pour analyse. Ne jamais embarquer de clés secrètes d'API tierces payantes en dur dans le code frontend.

---
*Ce document devra être révisé à chaque ajout majeur de fonctionnalité (ex: Authentification, Cloud Sync).*
