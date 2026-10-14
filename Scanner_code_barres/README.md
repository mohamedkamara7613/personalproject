# 📷 Scanner & Décodeur de Codes-Barres 1D en Vision par Ordinateur

[![Language](https://img.shields.io/badge/Language-C++17_%7C_Python-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)](https://en.wikipedia.org/wiki/C%2B%2B17)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![TIPE](https://img.shields.io/badge/Projet-CPGE_MP*-orange?style=for-the-badge)](#)

Projet de Travail d'Initiative Personnelle Encadré (**TIPE en CPGE MP***).  
Conception d'un algorithme robuste de **localisation, redressement et décodage de codes-barres 1D (EAN-13)** à partir d'images prises dans des conditions réelles dégradées (faible contraste, orientation oblique, flou optique, courbure d'emballage).

---

## 👁️ Pipeline de Traitement d'Image

```
          Image brute acquise
                   │
                   ▼
       [   Prétraitement & Débruitage   ] ──► Filtre bilatéral / Gaussien
                   │
                   ▼
       [ Détection de Gradient & Sobel  ] ──► Mise en valeur des barres verticales
                   │
                   ▼
       [ Morphologie Mathématique       ] ──► Fermeture morphologique pour fusionner les barres
                   │
                   ▼
       [ Détection de Contours & Bounding]──► Boîte englobante orientée (RotatedRect)
                   │
                   ▼
       [ Redressement Affine (Warp)     ] ──► Homographie & alignement horizontal
                   │
                   ▼
       [ Échantillonnage & Décodage     ] ──► Seuil d'Otsu + Décodage EAN-13 (Gardes & Chiffres)
```

---

## 🔬 Résultats Expérimentaux

Le système a été validé sur une base d'images tests présentant des angles de rotation variés et des dégradations lumineuses :
- Détection invariante à la rotation de $0^\circ$ à $360^\circ$.
- Décodage à $100\%$ sur des images contrastées et à plus de $92\%$ sur des images floues ou bruitées grâce au fenêtrage dichotomique adaptatif.

Les résultats de segmentation par fenêtrage se trouvent dans le sous-dossier `Test/img/window/`.

---

## 📑 Présentation & Rapports Académiques (TIPE)
- 📊 [Consulter le Diaporama de Présentation Officiel TIPE (PDF)](./docs/Presentation_TIPE_CodeBarres.pdf)
- 📋 [Consulter le Dossier MCOT - Mise en Cohérence des Objectifs TIPE (PDF)](./docs/MCOT_TIPE_CodeBarres.pdf)
