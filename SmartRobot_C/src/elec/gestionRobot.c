/**
 * @file gestionRobot.c
 * @brief Contrôle des moteurs et déplacements du robot.
 */

#include <wiringPi.h>
#include <stdbool.h>
#include <stdio.h>
#include "initVarRobot.h"
#include "lcd_display.h"

/**
 * @brief Initialise les broches du robot.
 *
 * Configure les capteurs, moteurs, PWM et buzzer.
 */
void setupPin() {
    wiringPiSetup();
    pinMode(CAPTEUR_LIGNE_GAUCHE, INPUT);
    pinMode(CAPTEUR_LIGNE_DROIT, INPUT);
    pinMode(CAPTEUR_LIGNE_MILIEU, INPUT);
    pinMode(EN1, PWM_OUTPUT);
    pinMode(EN2, PWM_OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    pinMode(BUZZER_PIN,OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);
}

/**
 * @brief Définit la vitesse des moteurs.
 *
 * @param vitesse Vitesse en pourcentage (0–100).
 */
void setSpeed(float vitesse) {
    pwmWrite(EN1, 10.24 * vitesse);
    pwmWrite(EN2, 10.24 * vitesse);
}

/**
 * @brief Fait avancer le robot.
 */
void avance() {
    setSpeed(VITESSE * 0.7);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
}

/**
 * @brief Fait tourner le robot à gauche.
 */
void gauche() {
    setSpeed(VITESSE * 0.60);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}

/**
 * @brief Fait tourner le robot à droite.
 */
void droite() {
    setSpeed(VITESSE * 0.60);

    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
}

/**
 * @brief Arrête les moteurs sans frein.
 */
void stop() {
    setSpeed(0);

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

/**
 * @brief Arrête les moteurs avec freinage actif.
 */
void stopFrein() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, HIGH);
}

/**
 * @brief Indique si le robot est sur la ligne.
 *
 * @return true si la ligne est détectée.
 */
bool surLigne() {
    return digitalRead(CAPTEUR_LIGNE_MILIEU);
}

/**
 * @brief Indique si le robot est sur une intersection.
 *
 * @return true si une intersection est détectée.
 */
bool surIntersection() {
    return (digitalRead(CAPTEUR_INTERSECTION_GAUCHE) || digitalRead(CAPTEUR_INTERSECTION_DROIT));
}

/**
 * @brief Tourne à gauche jusqu’à retrouver la ligne.
 *
 * @param delais Délai avant la rotation (ms).
 */
void gaucheTrouverLigne(int delais) {
    delay(delais);
    gauche();
    while (!surLigne()){
        //delay(DELAIS_LECTURE); // Delay pas forcément nécessaire
    }
}

/**
 * @brief Gère un virage à gauche à une intersection.
 *
 * @param delais Délai avant action (ms).
 */
void gaucheIntersection(int delais) {
    delay(delais);
    gauche();
    while (surLigne()){
        //delay(50); // Delay pas forcément nécessaire
    }

    gaucheTrouverLigne(0);
    droite();
    delay(OPPOSEE);
    stop();
}

/**
 * @brief Tourne à droite jusqu’à retrouver la ligne.
 *
 * @param delais Délai avant la rotation (ms).
 */
void droiteTrouverLigne(int delais) {
    delay(delais);
    droite();
    while (!surLigne()){
        //delay(DELAIS_LECTURE); // Delay pas forcément nécessaire
    }
}

/**
 * @brief Gère un virage à droite à une intersection.
 *
 * @param delais Délai avant action (ms).
 */
void droiteIntersection(int delais) {
    delay(delais);
    droite();

    while (surLigne()){
  //      delay(50); // Delay pas forcément nécessaire
    }
    droiteTrouverLigne(0);

    gauche();
    delay(OPPOSEE);
    stop();
}

/**
 * @brief Suit la ligne jusqu’à une intersection.
 *
 * Ajuste la trajectoire en fonction des capteurs.
 *
 * @param delais Délai initial (ms).
 */
void gestionSuiviLigne(int delais) {
    avance();
    //delay(150);

    while (!surIntersection()){
        if (digitalRead(CAPTEUR_LIGNE_GAUCHE) && (!digitalRead(CAPTEUR_LIGNE_MILIEU))){
            gauche();
        } else if ((!digitalRead(CAPTEUR_LIGNE_MILIEU)) && digitalRead(CAPTEUR_LIGNE_DROIT)){
            droite();
        } else {
            avance();
        }
    }
}

/**
 * @brief Exécute une instruction à une intersection.
 *
 * @param instruct
 * - 0 : Avancer
 * - 1 : Tourner à gauche
 * - 2 : Tourner à droite
 */
void gestionIntersection(int instruct) {
    switch (instruct) {
        case 0:
            gestionSuiviLigne(DELAIS_INTERSECTION);
            break;
        case 1:
            gaucheIntersection(DELAIS_INTERSECTION);
            break;
        case 2:
            droiteIntersection(DELAIS_INTERSECTION);
            break;
        default:
            printf("Instruction invalide");
    }
}
