# Règles de Développement & Comportement (WakhMu)

Ce fichier centralise nos règles communes de développement pour garantir la cohérence du projet WakhMu. Il est lié à l'état du projet via [[Project_State]].

## 🎨 1. Design & UI
- Toujours privilégier une esthétique premium, élégante et islamique (inspirée des maquettes *Innovation Mouride*).
- Palette de couleurs : Tons marrons foncés, beige/doré (`#C8832A`), fond crème pour la lecture (`#FAF6F0`).
- **Police Arabe** : Utilisation exclusive de la police **Amiri** pour garantir une clarté et un support parfait des diacritiques.
- Animations : Privilégier des animations fluides (pulsations douces, ondes sonores) pour l'interaction.

## 🛠️ 2. Stack Technique (Frontend)
- **Vite + React** : Pour un build rapide et une compatibilité maximale.
- **Zustand** : Pour la gestion de l'état global. Pas de Redux, rester simple.
- **Dexie.js** : Pour stocker les données persistantes locales (Historique, Favoris) afin de garantir une expérience offline-first fluide.
- **CSS Natif** : Utilisation de variables CSS (`var(--color-bg)`). Pas de framework CSS externe lourd sans nécessité absolue.
- **Mobile First** : L'interface doit être conçue en priorité pour un format mobile (PWA ou Capacitor).

## 🔒 3. Sécurité & Bonnes Pratiques
- Se référer en permanence au fichier [[docs/SECURITE.md]].
- Ne jamais stocker de données sensibles dans le LocalStorage.
- Veiller à bien demander la permission d'accès au micro de façon transparente (Principe du moindre privilège).

## 🤖 4. Workflow Agent IA (Obsidian)
- Documenter l'évolution globale du projet dans le fichier [[Journal_Evolution]].
- Garder le fichier [[Project_State]] systématiquement à jour après chaque réalisation.
- Utiliser la syntaxe wiki `[[NomDuFichier]]` pour interconnecter la documentation et assurer une traçabilité sur la vue graphique Obsidian.
- Placer les brouillons et tâches obsolètes dans le répertoire `[[Archive/]]`.
