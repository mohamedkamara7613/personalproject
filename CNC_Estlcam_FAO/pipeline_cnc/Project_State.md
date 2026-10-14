# 🧠 Project State — Pipeline CNC (Intégration FAO↔Machine)

> **Dernière mise à jour :** 2026-07-07  
> **Statut global :** 🔴 Bloquant — Problème axe Z + défaillance hardware boutons DDCS

---

## 🎯 Objectif du projet

Configurer et valider le pipeline logiciel complet permettant à un ami de passer de son dessin (SketchUp) à l'exécution d'un usinage sur sa CNC **QueenBee Pro**, en passant par **Estlcam** (FAO) et le contrôleur **DDCS V3**.

👉 Voir la fiche de ligne directrice : [[Fiche_Objectif_Ligne_Directrice]]

---

## 🔗 Matériel concerné

| Élément | Rôle dans le pipeline |
|---|---|
| **SketchUp** | CAO — Création du modèle 3D |
| **Estlcam** | FAO — Génération du G-code |
| **DDCS4 V3.1** | Contrôleur autonome — Lit la clé USB |
| **QueenBee Pro** | Machine CNC à fraiser |

---

## 📋 Phases du projet

- [x] Phase 0 — Compréhension du besoin (discussion initiale)
- [x] Phase 1 — **Visite technique sur place** (audit machine + récupération d'infos)
  - Checklist dans : [[Fiche_Questions_Inspection_Visite]]
- [x] Phase 2 — Configuration Estlcam (post-processeur + outils)
  - Guide dans : [[Fiche_Configuration_Technique]]
- [x] Phase 3 — Tests à vide (Air cutting) sur DDCS V3 ✅
- [/] Phase 4 — Premier usinage réel (MDF) — ⚠️ XY OK / Z incorrect → en diagnostic
  - Voir entrée [[Journal_Evolution]] du 2026-06-30
- [ ] Phase 5 — Rédaction du Mode Opératoire Standard (SOP) pour l'ami

---

## 📁 Fichiers du projet

| Fichier | Description |
|---|---|
| [[Fiche_Objectif_Ligne_Directrice]] | La vision globale du projet, à relire en cas de doute |
| [[Fiche_Configuration_Technique]] | Guide pas-à-pas pour configurer Estlcam + DDCS |
| [[Fiche_Questions_Inspection_Visite]] | Toutes les questions & vérifications à faire sur place |
| [[Projet_Couvercle_Plexi]] | Dossier technique sur le couvercle et l'incrustation du plexiglas |
| [[Fiche_Post_Forum_Bug_Z]] | Post forum rédigé pour le diagnostic du bug profondeur Z |
| [[Fiche_Reponse_Forum_Kevin]] | Réponse au forum — Kevin + Jbaero + Jean-Pierre |
| [[Fiche_Calibration_Steps_Z]] | 🔴 Procédure de calibration Steps/mm axe Z — à faire sur machine |
| [[Fiche_Reset_DDCS]] | **(Nouveau)** Version réelle DDCS4 V3.1 + options reset + analyse boutons |
| [[Rules]] | Règles de travail et conventions |
| [[Journal_Evolution]] | Journal des décisions et des apprentissages |

---

## ⚠️ Points bloquants actuels

- [x] Valider si le projet est **2.5D ou 3D** → 2.5D confirmé ✅
- [x] Récupérer les références des fraises disponibles dans l'atelier ✅
- [x] Poster sur forum pour diagnostic → 3 experts répondent : consensus Steps/mm Z ✅
- [x] **Correction version :** le DDCS est un **DDCS4 V3.1** (pas V3.3) — corrigé dans toutes les fiches ✅
- [ ] 🔴 **[ACTION 1]** Sauvegarder le fichier `setting.set` actuel avant tout reset
  - Procédure dans [[Fiche_Reset_DDCS]]
- [ ] 🔴 **[ACTION 2]** Faire le **test de calibration Steps/mm Z** avec pied à coulisse
  - Commander 20mm sur le DDCS en manuel → mesurer la distance réelle
  - Procédure dans [[Fiche_Calibration_Steps_Z]]
- [ ] 🔴 **[ACTION 3]** Diagnostiquer les boutons défaillants (SELECT, navigation USB, commandes)
  - Analyse dans [[Fiche_Reset_DDCS]] — probablement matériel, le reset ne suffit pas
  - Si reset paramètres ne suffit pas → contacter Digital Dream (info@ddcnc.com)
- [ ] 🟡 **[SECONDAIRE]** Vérifier le câblage moteur Z (faux contact) — après calibration
