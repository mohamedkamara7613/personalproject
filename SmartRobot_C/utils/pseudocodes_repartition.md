# Repartition du boulot entre Mohamed et Fakhoury

---

## Hypothèse structurante

**Le labyrinthe est représenté comme un graphe étendu** :
Chaque nœud = `(caseID, orientation)`
Chaque arc possède un coût = `turnCost` + `avCost`.

Donc tout calcul de chemin tient déjà compte de l’orientation.

---

# **ALGORITHME PRINCIPAL : `chercherCheminOptimal`**

```
procedure chercherCheminOptimal(fichier, turnCost, avCost)
    // 1. Parser → construit le Labyrinthe étendu
    (lab, startCase, startOrient, checkpoints) <- Parser(fichier)

    // 2. Construction de l’ensemble des points S
    (S, indexOf) <- BuildPointSet(startCase, checkpoints)

    // 3. Calcul de tous les plus courts chemins entre les points de S
    (dist, parent) <- AllPairsShortestPaths(lab, S)

    // 4. Construction matrice de coût asymétrique pour l’ATSP
    C <- ComputeCostMatrix(dist)

    // 5. Résolution ATSP (exact si peu de points, sinon heuristique)
    si taille(S) <= 15 alors
        order <- HeldKarpATSP(C)
    sinon
        order <- HeuristicATSP(C)
    fin si

    // 6. Reconstitution du chemin complet dans le graphe
    fullPath <- ReconstructFullPath(order, S, parent)

    // 7. Conversion du chemin en liste d’instructions robot
    instructions <- ConvertPathToInstructions(fullPath, startOrient)

    retourner instructions
fin
```

---

# **DÉTAIL DES FONCTIONS )**

---

## 1) **Parser**

Entrée : fichier texte
Sorties :

* `lab` : graphe étendu prêt à l’emploi
* `startCase`
* `startOrient`
* `checkpoints` (liste des cases à visiter)

```
procedure Parser(fichier)
    lire largeur
    initialiser lab avec largeur

    pour chaque case du fichier
        ajouter les sommets (caseID, orientation)
    fin pour

    pour chaque passage
        créer arcs (caseID, orient) → (voisinID, nouvelleOrient) avec coûts appropriés
    fin pour

    lire startCase, startOrient
    lire checkpoints

    retourner (lab, startCase, startOrient, checkpoints)
fin
```

---

## 2) **BuildPointSet**

Entrée : startCase, checkpoints
Sorties : S = [startCase, checkpoint1, …], et indexOf

```
procedure BuildPointSet(startCase, checkpoints)
    S <- liste vide
    ajouter startCase dans S
    pour chaque c dans checkpoints
        ajouter c dans S
    fin pour
    construire un dictionnaire indexOf[c] = position dans S
    retourner (S, indexOf)
fin
```

---

## 3) **AllPairsShortestPaths**

Entrée : graphe étendu `lab`, ensemble S
Sorties :

* dist[i][j]
* parent[i][j] : pour reconstruire les chemins

```
procedure AllPairsShortestPaths(lab, S)
    pour i de 0 à taille(S)-1
        (dist[i], parent[i]) <- Dijkstra(lab, S[i])
    fin pour
    retourner (dist, parent)
fin
```

---

## 4) **ComputeCostMatrix**

```
procedure ComputeCostMatrix(dist)
    pour i de 0 à n-1
        pour j de 0 à n-1
            si i = j alors C[i][j] <- INF
            sinon C[i][j] <- dist[i][j]
        fin pour
    fin pour
    retourner C
fin
```

---

## 5) **HeldKarpATSP (exact)**

```
procedure HeldKarpATSP(C)
    // DP bitmask classique
    retourner ordre optimal
fin
```

## 6) **HeuristicATSP (si n trop grand)**

```
procedure HeuristicATSP(C)
    // ex : nearest neighbor + 2-opt
    retourner ordre approximé
fin
```

---

## 7) **ReconstructFullPath**

```
procedure ReconstructFullPath(order, S, parent)
    fullPath <- liste vide

    pour k de 0 à taille(order)-2
        i <- order[k]
        j <- order[k+1]
        chemin_ij <- reconstruireChemin(parent[i], S[i], S[j])
        concatener chemin_ij à fullPath
    fin pour

    retourner fullPath
fin
```

---

## 8) **ConvertPathToInstructions**

```
procedure ConvertPathToInstructions(fullPath, startOrient)
    orientCourant <- startOrient
    instructions <- liste vide

    pour chaque transition (case,orient) -> (case2,orient2)
        si orient2 ≠ orientCourant
            générer TG ou TD nécessaires
            orientCourant <- orient2
        fin si
        ajouter "AV"
    fin pour

    retourner instructions
fin
```

---

# 2) RÉPARTITION DU TRAVAIL EN DEUX PERSONNES

### Version claire, équilibrée, et *réaliste pour un projet de groupe*

---

# **PERSONNE A — “Architecture & Modélisation du Labyrinthe”**

Travail : *tout ce qui construit le monde, les structures et les états.*

### Partie A doit coder :

### 1) **Tous les TAD**

* TAD Direction
* TAD Case
* TAD ListeChainee (déjà fourni → intégrer proprement)
* TAD Labyrinthe (version étendue)

### 2) **Parser**

* lecture du fichier
* création du graphe étendu
* conversion des passages en arcs `(case, orientation)`
* intégration `startCase`, `startOrient`, `checkpoints`

### 3) **BuildPointSet**

### 4) **Vérification et outils internes**

### 5) **Dijkstra (sur le graphe étendu)**

→ utilise les fonctions du TAD Labyrinthe
→ génère dist + parent

* fonctions d’aide (coordonnées, orientation, voisins, etc.)

### Objectif de la personne A :

> **Fournir un Labyrinthe étendu parfaitement construit, cohérent, vérifiable, et utilisable par Dijkstra.**

Cette partie est structurelle :
si A fait bien son travail → B n’a AUCUN BUG.

---

# **PERSONNE B — “Recherche du chemin optimal & logique algorithmique”**

Travail : *tout ce qui concerne les algorithmes avancés.*

### Partie B doit coder :

### 2) **AllPairsShortestPaths**

### 3) **ComputeCostMatrix**

### 4) **HeldKarpATSP**

### 5) **HeuristicATSP**

### 6) **ReconstructFullPath**

* reconstituer les chemins entre points ATSP
* concaténer

### 7) **ConvertPathToInstructions**

* gestion des rotations
* production AV/TG/TD

### Objectif de la personne B :

> **Transformer le labyrinthe étendu en une solution optimale et la convertir en instructions robot.**

---

# BONUS : Schéma de répartition (clair)

```
PERSONNE A : Fakhoury              PERSONNE B : Mohamed
-------------------------------------------------------------
TAD Direction                  
TAD Case                        AllPairsShortestPaths
TAD Labyrinthe étendu

                                ComputeCostMatrix
Parser                          HeldKarpATSP
BuildPointSet                   HeuristicATSP
Dijkstra                        ReconstructFullPath
                               ConvertPathToInstructions
```

---

# 3) Elec

---

## 1) **InitVarRobot**

```
CONSTANTE CAPTEUR_INTERSECTION_GAUCHE <- 27
CONSTANTE CAPTEUR_INTERSECTION_DROIT <- 22

CONSTANTE CAPTEUR_LIGNE_GAUCHE <- 21
CONSTANTE CAPTEUR_LIGNE_DROIT <- 5
CONSTANTE CAPTEUR_LIGNE_MILIEU <- 20

CONSTANTE EN1 <- 23
CONSTANTE EN2 <- 26

// Moteur gauche
CONSTANTE IN1 <- 2
CONSTANTE IN2 <- 3

// Moteur droit
CONSTANTE IN3 <- 6
CONSTANTE IN4 <- 25

// Paramètres robot
CONSTANTE VITESSE <- 80
CONSTANTE DELAIS_INTERSECTION <- 0
CONSTANTE DELAIS_ROTATION <- 0
CONSTANTE DELAIS_LECTURE <- 10
```

---

## 2) **Etat Capteur**

```
type EtatCapteur = Structure
    ligneGauche : Booleen
    ligneMilieu : Booleen
    ligneDroit : Booleen
    intersectionGauche : Booleen
    intersectionDroit : Booleen
fin Structure

fonction obtenirEtatCapteur() : EtatCapteur
    debut
        declaration e : EtatCapteur

        e.ligneGauche <- lireCapteur(CAPTEUR_LIGNE_GAUCHE)
        e.ligneMilieu <- lireCapteur(CAPTEUR_LIGNE_MILIEU)
        e.ligneDroit <- lireCapteur(CAPTEUR_LIGNE_DROIT)

        e.intersectionGauche <- lireCapteur(CAPTEUR_INTERSECTION_GAUCHE)
        e.intersectionDroit <- lireCapteur(CAPTEUR_INTERSECTION_DROIT)

        retourner e
    fin

```

---

## 3) **Instruction** 

```
type Instruction = Enumeration
    AV
    TG
    TD
fin Enumeration
```

---

## 4) **Gestion Robot**

```
procedure setupPin()
    debut
        initialisationWiringPi()
        modePin(CAPTEUR_LIGNE_GAUCHE, ENTREE)
        modePin(CAPTEUR_LIGNE_DROIT, ENTREE)
        modePin(CAPTEUR_LIGNE_MILIEU, ENTREE)

        modePin(EN1, SORTIE_PWM)
        modePin(EN2, SORTIE_PWM)
        modePin(IN1, SORTIE)
        modePin(IN2, SORTIE)
        modePin(IN3, SORTIE)
        modePin(IN4, SORTIE)
    fin

procedure setSpeed(vitesse : reel)
    debut
        ecrirePWM(EN1, 10.24 * vitesse)
        ecrirePWM(EN2, 10.24 * vitesse)
    fin

procedure avance()
    debut
        setSpeed(VITESSE * 0.7)
        ecrirePin(IN1, LOW)
        ecrirePin(IN2, HIGH)
        ecrirePin(IN3, LOW)
        ecrirePin(IN4, HIGH)
    fin

procedure gauche()
    debut
        setSpeed(VITESSE * 0.6)
        ecrirePin(IN1, LOW)
        ecrirePin(IN2, HIGH)
        ecrirePin(IN3, HIGH)
        ecrirePin(IN4, LOW)
    fin

procedure droite()
    debut
        setSpeed(VITESSE * 0.6)
        ecrirePin(IN1, HIGH)
        ecrirePin(IN2, LOW)
        ecrirePin(IN3, LOW)
        ecrirePin(IN4, HIGH)
    fin

procedure stop()
    debut
        setSpeed(0)
        ecrirePin(IN1, LOW)
        ecrirePin(IN2, LOW)
        ecrirePin(IN3, LOW)
        ecrirePin(IN4, LOW)
    fin

fonction surLigne() : Booleen
    debut
        retourner lecturePin(CAPTEUR_LIGNE_MILIEU)
    fin

fonction surIntersection() : Booleen
    debut
        retourner lecturePin(CAPTEUR_INTERSECTION_GAUCHE) OU lecturePin(CAPTEUR_INTERSECTION_DROIT)
    fin

procedure gestionSuiviLigne(delais : entier)
    debut
        avance()
        tant que NON surIntersection() faire
            si lecturePin(CAPTEUR_LIGNE_GAUCHE) ET NON lecturePin(CAPTEUR_LIGNE_MILIEU) alors
                gauche()
            sinon si lecturePin(CAPTEUR_LIGNE_DROIT) ET NON lecturePin(CAPTEUR_LIGNE_MILIEU) alors
                droite()
            sinon
                avance()
            fin si
            attendre(delais)
        fin tant que
    fin

procedure gaucheIntersection(delais : entier)
    debut
        attendre(delais)
        gauche()
        tant que surLigne() faire
            // attendre
        fin tant que
        stop()
    fin

procedure droiteIntersection(delais : entier)
    debut
        attendre(delais)
        droite()
        tant que surLigne() faire
            // attendre
        fin tant que
        stop()
    fin

procedure gestionIntersection(instr : entier)
    debut
        selon instr faire
            cas 0 : gestionSuiviLigne(DELAIS_INTERSECTION)
            cas 1 : gaucheIntersection(DELAIS_INTERSECTION)
            cas 2 : droiteIntersection(DELAIS_INTERSECTION)
            autre : ecrire("Instruction invalide")
        fin selon
    fin


```
---

## 5) **Buzzer** 

```
procedure buzzer_beep_ms(dureeMs : entier)
    debut
        ecrirePin(BUZZER_PIN, HIGH)
        attendre(dureeMs)
        ecrirePin(BUZZER_PIN, LOW)
    fin
```

---

## 6) **LCD**

```
CONSTANTE AF_BASE <- 64
CONSTANTE AF_RS <- AF_BASE + 0
CONSTANTE AF_RW <- AF_BASE + 1
CONSTANTE AF_E  <- AF_BASE + 2
CONSTANTE AF_LED <- AF_BASE + 3
CONSTANTE AF_DB4 <- AF_BASE + 4
CONSTANTE AF_DB5 <- AF_BASE + 5
CONSTANTE AF_DB6 <- AF_BASE + 6
CONSTANTE AF_DB7 <- AF_BASE + 7

CONSTANTE LCD_COLS <- 16
CONSTANTE LCD_ROWS <- 2
CONSTANTE I2C_ADDR <- 0x27

déclaration lcdHandle : entier
déclaration lcdReady : Booleen

fonction setupLcd() : entier
    debut
        si lcdReady alors
            retourner 0
        fin si

        si pcf8574Setup(AF_BASE, I2C_ADDR) < 0 alors
            ecrire("Erreur setup pcf8574")
            retourner -1
        fin si

        lcdHandle <- lcdInit(LCD_ROWS, LCD_COLS, 4,
                             AF_RS, AF_E,
                             AF_DB4, AF_DB5, AF_DB6, AF_DB7,
                             0,0,0,0)

        si lcdHandle < 0 alors
            ecrire("Erreur lcdInit")
            retourner -1
        fin si

        // Configuration broches
        pour i de 0 à 7 faire
            modePin(AF_BASE + i, SORTIE)
        fin pour
        ecrirePin(AF_LED, HIGH)
        ecrirePin(AF_RW, LOW)

        lcdDisplay(lcdHandle, 1)
        lcdCursor(lcdHandle, 0)
        lcdClear(lcdHandle)
        lcdReady <- vrai
        retourner 0
    fin

procedure lcd_display_set_lines(line0 : chaine, line1 : chaine)
    debut
        si lcdReady = faux alors
            setupLcd()
        fin si
        lcdWriteLine(0, line0)
        lcdWriteLine(1, line1)
    fin

procedure lcd_display_set_line(row : entier, text : chaine)
    debut
        lcdWriteLine(row, text)
    fin

procedure afficher_LCD(ligne : entier, text : chaine)
    debut
        lcd_display_set_line(ligne, text)
    fin

```

---

## 7) **RGB**
```
déclaration capteur_initialise : Booleen <- faux
CONSTANTE delai_integration <- 200   // ms

// Seuils pour détection de couleur
CONSTANTE seuil_noir <- 120
CONSTANTE seuil_blanc <- 215
CONSTANTE tol_balance_blanc <- 0.12
CONSTANTE ratio_dom_couleur <- 1.4
CONSTANTE delta_dom_couleur <- 25
CONSTANTE niveau_min_couleur <- 70
CONSTANTE ratio_vert_strict <- 1.6
CONSTANTE delta_vert <- 35
CONSTANTE saturation_min <- 0.20

fonction initialiser_capteur_rgb()
    debut
        si capteur_initialise = vrai alors
            retourner
        fin si
        initialisationWiringPi()
        configurer_capteur_i2c()
        capteur_initialise <- vrai
    fin

fonction lire_couleur_rgb(sortie : RgbcValues)
    debut
        attendre(delai_integration)
        sortie.clear <- lire_clear()
        sortie.red <- lire_red()
        sortie.green <- lire_green()
        sortie.blue <- lire_blue()
    fin

fonction normaliser_rgb(raw : RgbcValues) : (r,g,b)
    debut
        si raw.clear = 0 alors
            retourner (0,0,0)
        fin si
        echelle <- 255 / raw.clear
        r <- min(raw.red * echelle, 255)
        g <- min(raw.green * echelle, 255)
        b <- min(raw.blue * echelle, 255)
        retourner (r,g,b)
    fin

fonction couleur_dominante(raw : RgbcValues) : chaine
    debut
        si raw.clear = 0 ou raw.clear < seuil_noir alors
            retourner "Noir"
        fin si

        (r,g,b) <- normaliser_rgb(raw)
        moyenne <- (r + g + b)/3
        maxc <- max(r,g,b)
        minc <- min(r,g,b)
        ecart_canaux <- maxc - minc
        saturation <- (maxc > 0) ? (maxc - minc)/maxc : 0

        si moyenne > seuil_blanc et ecart_canaux <= tol_balance_blanc * moyenne alors
            retourner "Blanc"
        fin si

        si saturation < saturation_min ou maxc < niveau_min_couleur alors
            retourner "None"
        fin si

        // Vérification couleur dominante
        seconde <- deuxième_valeur_max(r,g,b)
        si maxc < seconde * ratio_dom_couleur ou maxc - seconde < delta_dom_couleur alors
            retourner "None"
        fin si

        si maxc = g alors
            si g < seconde * ratio_vert_strict ou g - seconde < delta_vert alors
                retourner "None"
            fin si
            retourner "Vert"
        fin si

        si maxc = r alors
            retourner "Rouge"
        sinon
            retourner "Bleu"
    fin

procedure afficher_couleur()
    debut
        variable v : RgbcValues
        lire_couleur_rgb(v)
        couleur <- couleur_dominante(v)

        si couleur = "Vert" ou couleur = "Rouge" alors
            afficher_LCD(0, couleur)
            buzzer_beep_ms(100)
            attendre(300)
        fin si
    fin

procedure boucle_thread_rgb(delai_ms : entier)
    debut
        initialiser_capteur_rgb()
        tant que vrai faire
            afficher_couleur()
            attendre(delai_ms)
        fin tant que
    fin
```

---

## 8) **Main Elec**
```
fonction charger_instructions_dynamique(flux, nb_instructions_sortie) : tableau de chaines
    debut
        capacite <- 10
        nb_lues <- 0
        instructions <- creer_tableau(capacite)

        tant que lire_mot(flux, mot_temporaire) faire
            si nb_lues >= capacite alors
                capacite <- capacite * 2
                instructions <- agrandir_tableau(instructions, capacite)
            fin si
            instructions[nb_lues] <- copier_chaine(mot_temporaire)
            nb_lues <- nb_lues + 1
        fin tant que

        nb_instructions_sortie <- nb_lues
        retourner instructions
    fin

fonction principale main() : entier
    debut
        debut_temps <- temps_actuel_millis()
        
        setupPin()
        lcd_display_init()

        nb_instr <- 0

        creer_thread(thread_RGB, rgb_color_thread_loop, NULL)

        instructions_robot <- charger_instructions_dynamique(stdin, nb_instr)
        ecrire("J'ai reçu " + nb_instr + " instructions.")

        pour i de 0 à nb_instr-1 faire
            ecrire("Instruction " + i + " : " + instructions_robot[i])
            
            si instructions_robot[i] = "AV" alors
                instr <- 0
                afficher_LCD(1,"Avancer")
            sinon si instructions_robot[i] = "TG" alors
                instr <- 1
                afficher_LCD(1,"Gauche")
            sinon si instructions_robot[i] = "TD" alors
                instr <- 2
                afficher_LCD(1,"Droite")
            sinon
                ecrire("Instruction inconnue: " + instructions_robot[i])
                stop()
                continuer
            fin si

            gestionIntersection(instr)
        fin pour

        // Libération mémoire
        pour i de 0 à nb_instr-1 faire
            liberer(instructions_robot[i])
        fin pour
        liberer(instructions_robot)

        afficher_LCD(0,"Circuit")

        fin_temps <- temps_actuel_millis()
        duree <- (fin_temps - debut_temps)/1000.0  // conversion en secondes
        afficher_LCD(1, convertir_en_chaine(duree) + " s")

        ecrire("Durée totale : " + convertir_en_chaine(duree) + " secondes")
        
        attendre_thread(thread_RGB)
        stop()

        retourner 0
    fin
```