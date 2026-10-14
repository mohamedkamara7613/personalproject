# 📮 Fiche Post Forum — Bug Axe Z (Profondeur incorrecte)

> **Statut :** 🔵 Prêt à poster  
> **Cibles :** OpenBuilds Community | r/hobbycnc | r/CNC | Forum Estlcam  
> **Lié à :** [[Project_State]] | [[Journal_Evolution]]

---

## ✉️ Titre du post

**Anglais (OpenBuilds / Reddit) :**
> [DDCS V3 + Estlcam] Z-axis cutting wrong depth — XY path is correct, Z depth does not match programmed value

**Français (forum francophone) :**
> [DDCS V3 + Estlcam] Profondeur Z incorrecte à l'usinage — Le parcours XY est bon mais la profondeur ne correspond pas

---

## 📝 Corps du post — VERSION ANGLAISE

---

Hello everyone,

I am a beginner in CNC and I am trying to get my first real cuts working. I would appreciate any help diagnosing a Z-axis depth problem.

### My Setup

- **Machine :** QueenBee Pro (OpenBuilds-style router)
- **Controller :** DDCS V3.3 (standalone G-code controller, USB)
- **CAM Software :** Estlcam (post-processor: Mach3, output: `.nc` file, units: mm)
- **Spindle :** Connected via VFD
- **End mill :** 3.17 mm straight 2-flute bit (ST2F-D3.1-L17)
- **Material :** 12 mm MDF board

---

### What works ✅

- The XY path is **perfectly correct** : the shape I designed is followed accurately by the machine.
- The spindle starts and runs correctly.
- G-code loads and runs without errors on the DDCS.

---

### Problem ❌

**The Z depth (cutting depth) does not match what I programmed in Estlcam.**

Here is exactly what I do and what happens:

1. **Z zeroing method :** I manually jog the Z axis down until the end mill just touches the top surface of the MDF board (paper method — a sheet of paper just barely slides under the bit). I then set Z=0 at that position on the DDCS.
2. **Estlcam settings :**
   - Step-down (Z+ / depth per pass) : `1.5 mm`
   - Total depth : e.g. `6 mm` for a pocket, or `12.2 mm` for a full cut-through
   - Safe Z (clearance plane) : `10 mm`
3. **Result :** The actual cut depth on the MDF does **not match** the programmed depth. The depth is visibly wrong (cuts too shallow or too deep — hard to quantify precisely without a caliper, will measure and update).

---

### Second related issue ⚠️ — Intermittent Z-axis random movement

Separately, I have noticed that **the Z axis sometimes behaves erratically** (random unexpected movement or position loss). This does NOT happen every time — it is completely random. Sometimes the machine works fine for 10 minutes, then the issue appears on the next run.

My hypothesis: **loose connection / false contact** somewhere on the Z motor wiring or Z limit switch connector. The electrical installation was done by a hardware engineer and has not been thoroughly checked yet.

**Could this intermittent issue be the root cause of the wrong depths?**  
(i.e., is the motor losing steps randomly, causing a cumulative Z offset during the program?)

---

### My questions

1. **Z calibration :** What is the correct procedure to verify and calibrate the Z `steps/mm` on a DDCS V3? (I am not sure this was done by the hardware engineer who wired the machine.)
2. **Z=0 procedure :** Is zeroing Z at the **top surface of the material** correct? Or should it be at the table/spoilboard surface?
3. **False contact → depth error ?** Can a loose wire on the Z axis motor cause systematic depth errors (not just random jumps), through accumulated step loss?
4. Any other common causes of Z depth mismatch between Estlcam and DDCS that I should check first?

---

Thank you for your help. I can provide the G-code file, Estlcam screenshots, or DDCS parameter screenshots if needed.

---

## 📝 Corps du post — VERSION FRANÇAISE

---

Bonjour à tous,

Je suis débutant en CNC et je cherche de l'aide pour diagnostiquer un problème de profondeur sur l'axe Z.

### Ma configuration

- **Machine :** QueenBee Pro
- **Contrôleur :** DDCS V3.3 (contrôleur autonome, clé USB)
- **Logiciel FAO :** Estlcam (post-processeur : Mach3, fichier `.nc`, unités : mm)
- **Fraise :** 3,17 mm 2 dents droites (ST2F-D3.1-L17)
- **Matériau :** Plaque MDF 12 mm

---

### Ce qui fonctionne ✅

- Le parcours XY est **parfaitement correct** : la forme dessinée est bien suivie par la machine.
- La broche démarre et tourne correctement.
- Le G-code charge et s'exécute sans erreur sur le DDCS.

---

### Le problème ❌

**La profondeur de coupe (axe Z) ne correspond pas à ce que j'ai programmé dans Estlcam.**

Voici ma procédure exacte et ce que j'observe :

1. **Méthode de mise à zéro Z :** J'approche manuellement la fraise jusqu'à ce qu'elle effleure la surface du MDF (méthode feuille de papier). Je fais le Z=0 à ce niveau sur le DDCS.
2. **Paramètres Estlcam :**
   - Profondeur de passe (Z+) : `1,5 mm`
   - Profondeur totale : ex. `6 mm` pour une poche, ou `12,2 mm` pour une découpe traversante
   - Safe Z (dégagement) : `10 mm`
3. **Résultat :** La profondeur réelle dans le MDF **ne correspond pas** à la valeur programmée. La profondeur est visuellement incorrecte.

---

### Problème secondaire ⚠️ — Comportement erratique de l'axe Z

En parallèle, l'axe Z a parfois un comportement erratique (mouvement inattendu ou perte de position). Ce comportement est **aléatoire et intermittent** — parfois absent pendant toute une session, parfois présent.

Mon hypothèse : **faux contact électrique** sur le câblage du moteur Z ou du fin de course Z. L'installation a été câblée par un ingénieur hardware mais n'a pas encore été vérifiée en détail.

**Ce faux contact pourrait-il être la cause réelle des erreurs de profondeur ?** (perte de pas moteur cumulée pendant l'exécution du programme ?)

---

### Mes questions

1. **Calibration Steps/mm :** Quelle est la procédure pour vérifier et calibrer le Steps/mm de l'axe Z sur un DDCS V3.3 ? (Je ne suis pas certain que ça ait été fait.)
2. **Procédure Z=0 :** Est-ce correct de mettre le Z=0 sur la **surface du matériau** ? Ou faut-il le faire sur le plateau/spoilboard ?
3. **Faux contact → erreur de profondeur ?** Un mauvais contact sur le câblage moteur Z peut-il provoquer des erreurs de profondeur systématiques par perte de pas cumulée ?
4. Quelles autres causes classiques d'écart de profondeur entre Estlcam et le DDCS dois-je vérifier en priorité ?

Merci pour votre aide. Je peux fournir le fichier G-code, des captures d'écran Estlcam ou les paramètres DDCS si besoin.

---

## 📋 Checklist AVANT de poster

> Compléter ces infos pour rendre le post le plus utile possible

- [ ] Mesurer la profondeur réelle avec un pied à coulisse → noter : profondeur programmée **X mm** / profondeur réelle **Y mm**
- [ ] Ajouter une **photo de la pièce usinée** vue de côté (coupe transversale si possible)
- [ ] Ajouter une **capture d'écran Estlcam** montrant les paramètres de passe et le parcours
- [ ] Trouver et noter le paramètre **Steps/mm de l'axe Z** dans les menus DDCS (paramètre lié aux drivers moteur)
- [ ] Vérifier visuellement le câblage du moteur Z et du connecteur fin de course Z (serrage des borniers)

---

*→ Retour au tableau de bord : [[Project_State]]*
