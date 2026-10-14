# 🏰 Java Aventure — Jeu de Rôle & Design Patterns GoF

[![Language](https://img.shields.io/badge/Language-Java_21_LTS-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://www.oracle.com/java/)
[![Patterns](https://img.shields.io/badge/Design_Patterns-GoF-blue?style=for-the-badge)](#)
[![SOLID](https://img.shields.io/badge/Principles-SOLID-brightgreen?style=for-the-badge)](#)

Jeu d'aventure textuel et interactif en Java illustrant l'application rigoureuse des principes de génie logiciel moderne : **SOLID**, architecture modulaire et patrons de conception du **Gang of Four (GoF)**.

---

## 📐 Design Patterns Appliqués

1. **Command Pattern :** Encapsulation de chaque action du joueur (`Aller`, `Prendre`, `Utiliser`, `Attaquer`) sous forme d'objet indépendant, permettant la gestion d'historique et l'annulation (*Undo/Redo*).
2. **State Pattern :** Modélisation des états du héros (Normal, Empoisonné, Équipé, Affaibli) influençant dynamiquement ses interactions.
3. **Factory Method :** Instanciation découplée des monstres, objets magiques et salles du donjon.
4. **Observer Pattern :** Système d'événements notifiant les entités lors des changements d'état de l'environnement (combat, découverte de secret).
