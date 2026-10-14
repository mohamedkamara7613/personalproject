# Compte Rendu d'Analyse — TP2 : Accéléromètre & Gyroscope (LSM6DSO)

**Auteur de l'analyse :** Antigravity  
**Date :** 25 février 2026  
**Sujet :** ITI3 Capteurs — TP2 Accéléromètre  
**Fichiers analysés :**
- `config/constants.py`
- `config/parameters.py`
- `sensors/IMU/accelerometer.py`
- `sensors/IMU/gyroscope.py`
- `sensors/IMU/imu.py`

---

## 1. Vue d'ensemble de l'architecture

Le projet est structuré de manière claire et modulaire :

```
TP2/
├── config/
│   ├── constants.py      # Adresses I2C, registres, tables de config
│   └── parameters.py     # Paramètres utilisateur (range, fréquence)
└── sensors/
    └── IMU/
        ├── imu.py        # Initialisation I2C + lecture brute + lecture IMU
        ├── accelerometer.py  # Config + lecture accéléromètre
        └── gyroscope.py      # Config + lecture gyroscope
```

Cette séparation est bonne : les **constantes hardware** sont isolées dans `constants.py`, les **paramètres configurables** dans `parameters.py`, et la **logique capteur** dans les modules IMU.

---

## 2. Analyse de `config/constants.py`

### ✅ Ce qui est correct

| Constante | Valeur | Cohérence |
|-----------|--------|-----------|
| `LSM6DSO_ADDR` | `0x6B` | ✅ Adresse I2C correcte (broche SA0 à VCC) |
| `LIS3MDL_ADDR` | `0x1E` | ✅ Adresse I2C correcte |
| `CTRL1_XL` | `0x10` | ✅ Registre correct selon datasheet LSM6DSO |
| `CTRL2_G` | `0x11` | ✅ Registre correct |
| `OUTX_L_A` | `0x28` | ✅ Premier registre de sortie accéléromètre |
| `OUTX_L_G` | `0x22` | ✅ Premier registre de sortie gyroscope |

### ⚠️ Problèmes identifiés dans `CONFIG_XL_FREQ`

Selon la datasheet du LSM6DSO (Table 46 - CTRL1_XL), les bits `ODR_XL[3:0]` sont :

| Fréquence (Hz) | Bits attendus | Valeur dans le code |
|----------------|--------------|---------------------|
| 12.5 | `0001` | ✅ `"0001"` |
| 26   | `0010` | ✅ `"0010"` |
| 52   | `0011` | ✅ `"0011"` |
| **104** | **`0100`** | ❌ `"0010"` **(doublon avec 26 Hz !)** | # OK merci mais je ne suis pas sûr que ça soit une erreur syntaxique python, d'aprés la datasheet des composants on a bien ces valeurs.
| 208  | `0101` | ✅ `"0101"` |
| 416  | `0110` | ✅ `"0110"` |
| 833  | `0111` | ✅ `"0111"` |
| 1660 | `1000` | ✅ `"1000"` |
| 3330 | `1001` | ✅ `"1001"` |
| 6660 | `1010` | ✅ `"1010"` |

> [!WARNING]
> **Bug critique ligne 18 :** La fréquence 104 Hz est mappée sur `"0010"` au lieu de `"0100"`. Cela signifie que configurer le capteur à 104 Hz écrira en réalité la valeur correspondant à 26 Hz dans le registre, provoquant une mauvaise fréquence d'acquisition silencieuse.

### ✅ `CONFIG_XL_RANGE` — Correct

Les bits `FS_XL[1:0]` dans CTRL1_XL :

| Range (g) | Bits | Valeur dans le code |
|-----------|------|---------------------|
| ±2  | `00` | ✅ |
| ±16 | `01` | ✅ |
| ±4  | `10` | ✅ |
| ±8  | `11` | ✅ |

### ✅ `CONFIG_XL_SENSITIVITY` — Correct (unité : mg/LSB)

| Range | Sensibilité (mg/LSB) | Code |
|-------|----------------------|------|
| ±2  | 0.061 | ✅ |
| ±4  | 0.122 | ✅ |
| ±8  | 0.244 | ✅ |
| ±16 | 0.488 | ✅ |

### ✅ `CONFIG_G_FREQ` — Correct

La table des fréquences gyroscope est cohérente avec la datasheet (bits `ODR_G[3:0]` dans CTRL2_G).

### ✅ `CONFIG_G_RANGE` — Correct (unité : dps)

| Range | Bits | Code |
|-------|------|------|
| 250  | `00` | ✅ |
| 500  | `01` | ✅ |
| 1000 | `10` | ✅ |
| 2000 | `11` | ✅ |

### ⚠️ `CONFIG_G_SENSITIVITY` — Valeur manquante

| Range (dps) | Sensibilité (mdps/LSB) | Code |
|-------------|------------------------|------|
| **125** | 4.375 | ⚠️ **La range 125 dps n'existe pas dans `CONFIG_G_RANGE`**, cette entrée est orpheline |
| 250  | 8.75  | ✅ |
| 500  | 17.5  | ✅ |
| 1000 | 35    | ✅ |
| 2000 | 70    | ✅ |

> [!NOTE]
> La clé `125` dans `CONFIG_G_SENSITIVITY` n'a pas de correspondant dans `CONFIG_G_RANGE`. Elle sera inaccessible via le code normal, sauf si la range 125 est ajoutée à `CONFIG_G_RANGE`. La range 125 dps est bien documentée dans la datasheet mais nécessite le bit FS_125 (bit 1 de CTRL2_G), ce qui est une configuration à part non gérée ici.

---

## 3. Analyse de `config/parameters.py`

```python
ACCEL_RANGE = 2       # ±2 g  → présent dans CONFIG_XL_RANGE ✅
ACCEL_FREQ  = 12.5    # Hz   → présent dans CONFIG_XL_FREQ ✅
GYRO_RANGE  = 250     # dps  → présent dans CONFIG_G_RANGE ✅
GYRO_FREQ   = 12.5    # Hz   → présent dans CONFIG_G_FREQ ✅
```

✅ Les paramètres par défaut sont cohérents avec les tables de `constants.py`. Toutes les clés existent dans les dictionnaires correspondants.

---

## 4. Analyse de `sensors/IMU/accelerometer.py`

### Fonction `accelerometer_configuration(accel_range, accel_freq)`

```python
CTRL1_XL = str(CONFIG_XL_FREQ[accel_freq]) + str(CONFIG_XL_RANGE[accel_range]) + "0" 
return bin(int(CTRL1_XL))
```
- correction
```python
CTRL1_XL = str(CONFIG_XL_FREQ[accel_freq]) + str(CONFIG_XL_RANGE[accel_range]) + "0" + "0"
return bin(int(CTRL1_XL))
```

**Logique attendue par le registre CTRL1_XL :**

```
Bits 7-4 : ODR_XL  (fréquence)       → 4 bits
Bits 3-2 : FS_XL   (range)           → 2 bits
Bit  1   : LPF2_XL_EN               → 1 bit (mis à 0, OK)
Bit  0   : (non utilisé)             → 1 bit (manquant !)
```

> [!CAUTION]
> **Bug de construction de la chaîne binaire :** `CTRL1_XL` est construit avec 4 + 2 + 1 = **7 bits** au lieu de 8. Le bit 0 (non utilisé, valeur `"0"`) est absent. Le registre devrait toujours être un entier 8 bits. De plus, `bin(int(CTRL1_XL))` interprète la chaîne comme un entier décimal (ex: `"000100 0"`) et non comme un nombre binaire — ce qui produira un résultat erroné.
>
> **Correction suggérée :**
> ```python
> CTRL1_XL = str(CONFIG_XL_FREQ[accel_freq]) + str(CONFIG_XL_RANGE[accel_range]) + "00"
> return int(CTRL1_XL, 2)  # Interpréter comme binaire, pas comme décimal
> ```

### Fonction `read_accelerometer(device_addr, accel_range)`

```python
sensitivity = (int(CONFIG_XL_RANGE[accel_range]) * int(CONFIG_XL_SENSITIVITY[accel_range]))
return x * sensitivity, y * sensitivity, z * sensitivity
```

> [!WARNING]
> **Erreur dans le calcul de la sensibilité :**
> - `CONFIG_XL_RANGE[accel_range]` renvoie une chaîne de bits (ex: `"00"` pour 2g)
> - `CONFIG_XL_SENSITIVITY[accel_range]` renvoie un float (ex: `0.061`)
> - `int("00") * 0.061 = 0` → **la sensibilité vaut toujours 0**, tous les axes retourneront 0 !
>
> **Correction attendue :** la sensibilité est directement dans `CONFIG_XL_SENSITIVITY`, pas besoin de multiplier par la range :
> ```python
> sensitivity = CONFIG_XL_SENSITIVITY[accel_range] 
> return x * sensitivity, y * sensitivity, z * sensitivity
> ```

---

## 5. Analyse de `sensors/IMU/gyroscope.py`

### Fonction `gyroscope_configuration(gyro_range, gyro_freq)`

```python
CTRL2_G = str(CONFIG_G_FREQ[gyro_freq]) + str(CONFIG_G_RANGE[gyro_range]) + str(0)
return bin(int(CTRL2_G))
```

**Même problème que `accelerometer_configuration` :**

> [!CAUTION]
> - 4 + 2 + 1 = **7 bits** construits au lieu de 8 pour le registre CTRL2_G
> - `bin(int(CTRL2_G))` interprète la chaîne comme un entier décimal — résultat incorrect
>
> **Correction suggérée :**
> ```python
> CTRL2_G = str(CONFIG_G_FREQ[gyro_freq]) + str(CONFIG_G_RANGE[gyro_range]) + "00"
> return int(CTRL2_G, 2)
> ```

### Fonction `read_gyroscope(device_addr, gyro_range)`

```python
sensitivity = (int(CONFIG_G_RANGE[gyro_range]) * int(CONFIG_G_SENSITIVITY[gyro_range]))
```

> [!WARNING]
> **Même erreur que pour l'accéléromètre :**
> - `CONFIG_G_RANGE[gyro_range]` retourne par exemple `"00"` pour 250 dps
> - `int("00") = 0` → **sensibilité toujours nulle**
> - De plus, `CONFIG_G_SENSITIVITY` contient des floats (`8.75`, `17.5`...) donc `int()` tronquerait les valeurs
>
> **Correction attendue :**
> ```python
> sensitivity = CONFIG_G_SENSITIVITY[gyro_range]  # ex: 8.75 mdps/LSB
> return x * sensitivity, y * sensitivity, z * sensitivity
> ```

---

## 6. Analyse de `sensors/IMU/imu.py`

### Initialisation I2C

```python
bus = smbus.SMBus(1)  # Bus I2C 1 (correcte pour RPi 4) ✅
```

### Fonction `initialize_sensors`

```python
bus.write_byte_data(XL_addr, CTRL1_XL, accelerometer_configuration(accel_range, accel_freq))
bus.write_byte_data(XL_addr, CTRL2_G, gyroscope_configuration(gyro_range, gyro_freq))
time.sleep(0.1)
```

> [!WARNING]
> **Problème de type de retour :** `accelerometer_configuration` et `gyroscope_configuration` retournent actuellement le résultat de `bin()`, soit une chaîne du type `'0b101...'`. Or `write_byte_data` attend un **entier** entre 0 et 255. Il faut que les fonctions de configuration retournent un `int`.
>
> Si les fonctions sont corrigées pour retourner `int(CTRL1_XL, 2)`, ce problème disparaît.

### Fonction `read_raw_data`

```python
data = bus.read_i2c_block_data(device_addr, start_register, 6)
x = data[0] | (data[1] << 8)
y = data[2] | (data[3] << 8)
z = data[4] | (data[5] << 8)
# Complément à 2
x = x - 65536 if x > 32767 else x
y = y - 65536 if y > 32767 else y
z = z - 65536 if z > 32767 else z
return x, y, z
```

✅ La lecture de 6 octets (2 par axe, little-endian) est correcte.  
✅ La conversion en valeur signée 16 bits par complément à deux est correcte.

### Fonction `read_IMU`

```python
accel_x,accel_y,accel_z = read_accelerometer(XL_addr, accel_range)
gyro_x,gyro_y,gyro_z = read_gyroscope(XL_addr, gyro_range)
return accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z
```

✅ Logique correcte. Les données sont bien agrégées.

---

## 7. Résumé des bugs identifiés

| # | Fichier | Ligne | Sévérité | Description |
|---|---------|-------|----------|-------------|
| 1 | `constants.py` | 18 | 🔴 Critique | `104 Hz` mappé sur `"0010"` au lieu de `"0100"` |
| 2 | `accelerometer.py` | 17,19 | 🔴 Critique | Registre à 7 bits au lieu de 8 + `bin(int(...))` interprète comme décimal |
| 3 | `accelerometer.py` | 35 | 🔴 Critique | `sensitivity` vaut toujours 0 (multiplication par `int("00")`) |
| 4 | `gyroscope.py` | 17,18 | 🔴 Critique | Même bug de construction de registre que l'accéléromètre |
| 5 | `gyroscope.py` | 34 | 🔴 Critique | `sensitivity` vaut toujours 0 (même bug) |
| 6 | `imu.py` | 23,24 | 🟠 Majeur | `write_byte_data` reçoit une chaîne `bin()` au lieu d'un entier |
| 7 | `constants.py` | 67 | 🟡 Mineur | Clé `125` dans `CONFIG_G_SENSITIVITY` sans correspondant dans `CONFIG_G_RANGE` |

---

## 8. Corrections recommandées

### `constants.py` — Corriger la fréquence 104 Hz

```python
# Ligne 18 — CORRECTION
104 : "0100",   # était "0010" (identique à 26 Hz) ❌
```

### `accelerometer.py` — Corriger les deux fonctions

```python
def accelerometer_configuration(accel_range, accel_freq):
    # Registre 8 bits : ODR[3:0] | FS[1:0] | LPF2 | 0
    CTRL1_XL = str(CONFIG_XL_FREQ[accel_freq]) + str(CONFIG_XL_RANGE[accel_range]) + "00"
    return int(CTRL1_XL, 2)  # Interpréter comme binaire

def read_accelerometer(device_addr, accel_range):
    from sensors.IMU import read_raw_data
    x, y, z = read_raw_data(device_addr, OUTX_L_A)
    sensitivity = CONFIG_XL_SENSITIVITY[accel_range]  # mg/LSB
    return x * sensitivity, y * sensitivity, z * sensitivity
```

### `gyroscope.py` — Corriger les deux fonctions

```python
def gyroscope_configuration(gyro_range, gyro_freq):
    # Registre 8 bits : ODR[3:0] | FS[1:0] | FS_125 | 0
    CTRL2_G = str(CONFIG_G_FREQ[gyro_freq]) + str(CONFIG_G_RANGE[gyro_range]) + "00"
    return int(CTRL2_G, 2)  # Interpréter comme binaire

def read_gyroscope(device_addr, gyro_range):
    from sensors.IMU import read_raw_data
    x, y, z = read_raw_data(device_addr, OUTX_L_G)
    sensitivity = CONFIG_G_SENSITIVITY[gyro_range]  # mdps/LSB
    return x * sensitivity, y * sensitivity, z * sensitivity
```

---

## 9. Conclusion

Le code suit une structure modulaire bien pensée et la logique globale (lecture I2C, conversion complément à deux, séparation config/capteur) est solide. Cependant, **plusieurs bugs critiques** empêchent le code de fonctionner correctement en l'état :

1. La **construction des octets de configuration** est incorrecte (7 bits au lieu de 8, interprétation décimale au lieu de binaire).
2. Le **calcul de la sensibilité** est erroné dans les deux capteurs — multiplier par `int(chaîne_binaire)` donne systématiquement 0.
3. Un **mapping de fréquence incorrect** (104 Hz ↔ `"0010"`) dans `CONFIG_XL_FREQ`.

Une fois ces corrections appliquées, le code sera fonctionnel pour communiquer avec le LSM6DSO via I2C sur une Raspberry Pi 4.
