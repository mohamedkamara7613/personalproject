# 🎧 Shazam Khassida (Wakhmu) — Reconnaissance Audio & Empreinte Acoustique

[![Language](https://img.shields.io/badge/Language-Python_3_%7C_React-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Front--End-React_%7C_Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)

Système complet d'identification et de reconnaissance d'enregistrements audio vocaux (Khassidas traditionnels), combinant un moteur d'empreinte acoustique spectrogramme, une base d'indexation inversée SQLite et une application moderne en **React / Vite**.

---

## 🎬 Démonstration de l'Application Web (Wakhmu)

![Wakhmu Demo](./docs/demo_wakhmu.gif)
*Interface mobile-first réactive : enregistrement micro, analyse en direct, identification de l'œuvre et affichage des métadonnées.*

---

## 🔬 Pipeline d'Empreinte Acoustique (Fingerprinting)

```
       Signal Audio brut (Microphone / Fichier)
                          │
                          ▼
        [ Filtrage Passe-Bande & STFT ]
                          │
                          ▼
        [ Extraction des Pics Spectraux (Constellation Map) ]
                          │
                          ▼
        [ Appariement de Paires de Pics (Hash = (f1, f2, Δt)) ]
                          │
                          ▼
        [ Recherche dans l'Index Inversé SQLite ]
                          │
                          ▼
        [ Alignement Temporel (Histogramme de décalage δt) ]
                          │
                          ▼
               Titre & Auteur Identifiés !
```

---

## 🚀 Lancement

### 1. Démarrer le Backend FastAPI
```bash
cd v1
pip install -r requirements.txt
python3 main.py
```

### 2. Démarrer l'application Web React
```bash
cd wakhmu
npm install
npm run dev
```
