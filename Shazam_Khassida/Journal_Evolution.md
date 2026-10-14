# Journal d'Évolution et Apprentissages

Ce document consigne l'historique des grandes décisions, pivots, impasses et réussites techniques rencontrés dans le développement de **WakhMu**. Il est connecté au tableau de bord [[Project_State]].

---

## Mai 2026 : Initialisation Frontend-First

- **Décision (Architecture)** : Devant la complexité de générer le dataset et d'entraîner le modèle IA (le *core*), nous avons décidé d'adopter une approche **Frontend-First / Mock-Driven**. Cela a permis de créer toute l'interface visuelle et fonctionnelle de WakhMu de manière indépendante avec de fausses données générées par un `mockAI`.
- **Réussite (Design)** : L'intégration du design system basé sur l'application *Innovation Mouride* a été un succès. La palette marron/doré et le mode de lecture (thème "Paper" avec police *Amiri*) offrent un rendu premium et apaisant. L'animation "ondes" du bouton d'écoute (Shazam) donne de la vie à l'interface.
- **Décision (Stack)** : Utilisation de la stack de *LifeCal* détaillée dans [[docs/TECH_STACK.md]] (React + Vite + Zustand + Dexie). Cette stack a prouvé sa rapidité de développement. Nous l'utiliserons en PWA d'abord, puis nous l'empaquetterons via Capacitor pour un déploiement natif.
- **Apprentissage (Sécurité)** : Il est nécessaire de cadrer la sécurité dès maintenant, en amont du branchement de l'IA, notamment pour le stockage local et les communications. Un rappel a été rédigé dans [[docs/SECURITE.md]].
- **Correction technique** : Lors du build Vite (esbuild/rollup), une erreur de parsing est survenue dans `src/data/khassidas.js` en raison de guillemets simples (`'`) non échappés dans les textes de translittération. **Leçon apprise :** Toujours utiliser des backticks (`` ` ``) ou des guillemets doubles pour les chaînes de caractères longues contenant des apostrophes (français ou translittération).

---

*(Prochaine étape : Définir la stratégie Dataset pour l'IA)*
