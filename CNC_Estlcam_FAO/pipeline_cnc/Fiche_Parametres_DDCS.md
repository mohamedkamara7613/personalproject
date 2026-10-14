# 🗂️ Fiche Paramètres DDCS — QueenBee Pro
> **Date de relevé :** 2026-07-16  
> **Source :** Photos écran DDCS (parametre_ddcs_1 à 13)  
> **Version firmware :** DDCSV3.3 @DREAM — Ver 2021-09-23-112NOR  
> **Lié à :** [[Project_State]] | [[Fiche_Calibration_Steps_Z]] | [[Fiche_Reset_DDCS]]

---

## 1. Paramètres Moteur — Steps/mm (#33 à #38)

> ⚠️ **Problème constaté le 2026-07-16 :** Les axes X et Y produisaient une découpe à l'échelle **1/2** (60mm au lieu de 120mm commandés). Cause : Steps/mm trop bas (100 au lieu de 200).

| N° | Paramètre | Valeur relevée | Valeur corrigée | Unité | Statut |
|---|---|---|---|---|---|
| **#33** | Motor start speed | 50.000 | 50.000 | unit/min | ✅ OK |
| **#34** | X axis pulse equivalency | 100.458 | **200** | P/unit | 🔴 À corriger |
| **#35** | Y axis pulse equivalency | 99.800 | **200** | P/unit | 🔴 À corriger |
| **#36** | Z axis pulse equivalency | 640.000 | à vérifier | P/unit | 🟡 À calibrer |
| **#38** | A axis pulse equivalency | 100.000 | N/A (non utilisé) | P/unit | — |

### Procédure de correction Steps/mm

**Sur le DDCS physique :**
1. Appuyer sur **Param Page**
2. Naviguer jusqu'au paramètre **#34** (Y+ / Y-)
3. Appuyer sur ENTER → modifier la valeur de `100` à `200`
4. ENTER pour valider
5. Répéter pour le **#35** : modifier `99.800` à `200`
6. Ne **pas** modifier #36 (Z) sans calibration physique préalable

**Formule de recalibration générale :**
```
Nouveau_Steps = Ancien_Steps × (Distance_commandée ÷ Distance_mesurée)
Exemple : 100 × (120 ÷ 60) = 200
```

---

## 2. Paramètres Broche (#98, #219 à #229)

| N° | Paramètre | Valeur relevée | Unité |
|---|---|---|---|
| **#98** | Maximum spindle speed | 24 000 | rpm |
| **#219** | If Stop Spindle when pause | No | — |
| **#220** | Spindle speed selection | G code | — |
| **#221** | Default spindle speed | 24 000 | rpm |
| **#222** | Spindle commands M3/M5 response | Yes | — |
| **#223** | Spindle M3/M4/M5 response Duration | 3.000 | s |
| **#224** | Spindle switch Active level | High | — |
| **#227** | Definition of PWM Electric level | 1111 | — |
| **#422** | PWM rising rate from 0V to 10V | 1 | — |
| **#433** | M4 pivot definition | No | — |

---

## 3. Paramètres Vitesse — Mode Manuel (#41, #103, #263–#265)

| N° | Paramètre | Valeur relevée | Unité |
|---|---|---|---|
| **#41** | X Axis max speed in M_Ctrl mode | 16 000 | unit/min |
| **#103** | A axis manual control speed | 12 000 | deg/min |
| **#263** | X axis stop Acc in M_Ctrl mode | 300 | unit/s² |
| **#264** | Y axis stop Acc in M_Ctrl mode | 150 | unit/s² |
| **#265** | Z axis stop Acc in M_Ctrl mode | 300 | unit/s² |
| **#266** | A axis stop Acc in M_Ctrl mode | 600 | deg/s² |

---

## 4. Paramètres Signaux Moteur (#390–#421)

| N° | Paramètre | Valeur relevée |
|---|---|---|
| **#390** | X axis DIR signal Electric Level | Low |
| **#391** | Y axis DIR signal Electric Level | Low |
| **#392** | Z axis DIR signal Electric Level | Low |
| **#393** | A axis DIR signal Electric Level | Low |
| **#416** | Time interval between DIR & pulse | 7 000 ns |
| **#418** | X axis Pulse signal Electric Level | Low |
| **#419** | Y axis Pulse signal Electric Level | Low |
| **#420** | Z axis Pulse signal Electric Level | Low |
| **#421** | A axis Pulse signal Electric Level | Low |

---

## 5. Paramètres Home / Zéro (#117–#126, #2024–#2028)

| N° | Paramètre | Valeur relevée |
|---|---|---|
| **#117** | Y axis zero signal source select | Z-limit signal |
| **#118** | Z axis zero signal source select | HOME signal |
| **#119** | A axis zero signal source select | Z-limit signal |
| **#126** | Home reminder after booting | No |
| **#2024** | X axis Home offset | 0.000 |
| **#2025** | Y axis Home offset | 0.000 |
| **#2026** | Z axis Home offset | 0.000 |
| **#2027** | A axis Home sequence | XYZA |
| **#2048** | Home sequence | mode 1 |

---

## 6. Paramètres Limites Logicielles (#375–#382)

| N° | Paramètre | Valeur relevée | Unité |
|---|---|---|---|
| **#375** | Soft-limited position value of X– | -400.000 | unit |
| **#376** | Soft-limited position value of Y– | -400.000 | unit |
| **#377** | Soft-limited position value of Z– | -20.000 | unit |
| **#378** | Soft-limited position value of A– | 0.000 | deg |
| **#379** | Soft-limited position value of X++ | 400.000 | unit |
| **#380** | Soft-limited position value of Y++ | 400.000 | unit |
| **#381** | Soft-limited position value of Z++ | 20.000 | unit |
| **#382** | Soft-limited position value of A++ | 0.000 | deg |
| **#374** | Enable software limit | Disable | — |
| **#2038** | Enable software limit alarm in idle state | Yes | — |

---

## 7. Paramètres Limites Matérielles (#407–#415)

| N° | Paramètre | Valeur relevée |
|---|---|---|
| **#407** | Limited signal active of A++ | Enable |
| **#408** | Effective electric level of X– | Low |
| **#409** | Effective electric level of Y– | Low |
| **#410** | Effective electric level of Z– | Low |
| **#411** | Effective electric level of A– | Low |
| **#412** | Effective electric level of X++ | Low |
| **#413** | Effective electric level of Y++ | Low |
| **#414** | Effective electric level of Z++ | Low |
| **#415** | Effective electric level of A++ | Low |

---

## 8. Paramètres Interpolation (#113, #124, #125)

| N° | Paramètre | Valeur relevée |
|---|---|---|
| **#113** | Arc interpolation algorithm selection | Soft algorithm |
| **#124** | Circular centrifugal acceleration | 0.000 |
| **#125** | Circular speed adjustment factor | 1.000 |

---

## 9. Paramètres Système (#1, #115, #2043)

| N° | Paramètre | Valeur relevée |
|---|---|---|
| **#115** | Unit selection | mm |
| **#16** | Current coordinate system | G54 |
| **#2043** | Subroutine programming mode | Disable |
| **#2031** | Uniaxial acc is limited by M_Ctrl start acc | No |
| **#2037** | Is FRO valid for G07 | No |
| **#435** | X axis protection speed | 99 999 |
| **#436** | Y axis protection speed | 99 999 |
| **#125** | Circular speed adjustment factor | 1.000 |

---

## 10. État actuel de la machine (page principale DDCS)

Coordonnées machine au moment du relevé :
| Axe | Position brute | Position affichée |
|---|---|---|
| X | 1218.454 | 38.365 mm |
| Y | -21.012 | 5.852 mm |
| Z | 632.650 | 21.420 mm |
| A | -2074.456 | 11.208 |

---

## 11. Journal des corrections Steps/mm

| Date | Axe | Valeur avant | Valeur après | Raison |
|---|---|---|---|---|
| 2026-07-16 | X (#34) | 100.458 | **200** | Découpe à l'échelle ×0.5 (60mm au lieu de 120mm) |
| 2026-07-16 | Y (#35) | 99.800 | **200** | Même problème que X |
| À faire | Z (#36) | 640.000 | À mesurer | Calibration physique avec pied à coulisse |

---

*→ Retour : [[Project_State]]*  
*→ Procédure calibration Z : [[Fiche_Calibration_Steps_Z]]*  
*→ Procédure reset/sauvegarde : [[Fiche_Reset_DDCS]]*
