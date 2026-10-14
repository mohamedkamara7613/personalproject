# 🎧 Shazam Khassida — Reconnaissance Audio & Empreinte Acoustique

[![Language](https://img.shields.io/badge/Language-Python_3-3670A0?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

Moteur de **reconnaissance acoustique (*Audio Fingerprinting*)** inspiré des algorithmes industriels (Shazam / Dejavu), adapté au traitement et à l'identification de chants et poèmes traditionnels (*Khassidas*).

---

## 🔬 Principe de l'Empreinte Acoustique

```
Extrait Audio Entrant (.wav, .mp3)
              │
              ▼
    [ Spectrogramme STFT ]  ──► Transformée temps-fréquence
              │
              ▼
    [ Extraction des Pics]  ──► Détection des maxima locaux d'énergie (constellation)
              │
              ▼
    [ Appariement de Pics]  ──► Création de paires (f1, f2, Δt) avec fenêtre cible
              │
              ▼
    [ Hachage Cryptographique]──► Hash = SHA1(f1 | f2 | Δt) associé au timestamp t1
              │
              ▼
    [ Index Inversé SQLite] ──► Recherche des collisions de hash & alignement temporel
```

---

## 🚀 Structure & Tests
- `v1/` : Implémentation du pipeline d'ingestion et d'empreintes.
- `wakhmu/` : Module de scraping et constitution du corpus audio.
- `test_db.py` : Validation des requêtes d'alignement temporel en base de données.
