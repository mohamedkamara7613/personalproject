# 📜 Rules — Conventions de Travail

> Lié à : [[Project_State]]

---

## Règles générales

1. **Toujours relire [[Project_State]] avant de commencer une session de travail**
2. **Ne jamais lancer un usiné réel sans test à vide (Air Cutting) préalable**
3. **Documenter chaque paramètre testé et son résultat dans [[Journal_Evolution]]**
4. **Lier tous les nouveaux fichiers à [[Project_State]] ou à une fiche existante**

## Conventions de nommage

- Fiches de référence : `Fiche_NomDescriptif.md`
- Fichiers G-code de test : `test_YYYYMMDD_description.nc`
- Archives : déposer dans `Archive/`

## Règles de sécurité machine (NON NÉGOCIABLES)

1. **E-Stop accessible à tout moment pendant l'usinage**
2. **Jamais les mains dans la zone de travail pendant que la broche tourne**
3. **Vérifier le Z=0 et le Safe Z avant tout lancement de programme**
4. **Commencer toujours avec un matériau test (mousse, bois de récupération)**

## Conventions Estlcam

- Unités : **toujours en millimètres**
- Post-processeur par défaut : **Mach3** (fallback : LinuxCNC)
- Extension G-code : **`.nc`**
- Safe Z minimum : **10 mm**
