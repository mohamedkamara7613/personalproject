/**
 * @file initVarRobot.h
 * @brief Définition des constantes matérielles et paramètres du robot.
 */
#ifndef INIT_VAR_ROBOT_H
#define INIT_VAR_ROBOT_H

/** Capteur d’intersection gauche */
#define CAPTEUR_INTERSECTION_GAUCHE 27

/** Capteur d’intersection droit */
#define CAPTEUR_INTERSECTION_DROIT 22

/** Capteur de ligne gauche */
#define CAPTEUR_LIGNE_GAUCHE 21

/** Capteur de ligne central */
#define CAPTEUR_LIGNE_MILIEU 0

/** Capteur de ligne droit */
#define CAPTEUR_LIGNE_DROIT 5

/** Enable moteurs (PWM) */
#define EN1 23
#define EN2 26

/** Moteur gauche - IN1 - IN2 */
#define IN1 2
#define IN2 3

/** Moteur droit - IN3 - IN4*/
#define IN3 6
#define IN4 25

/** Vitesse nominale du robot */
#define VITESSE 70

/** Délai entre deux lectures capteurs (ms) */
#define DELAIS_LECTURE 25

/** Broche du buzzer */
#define BUZZER_PIN 29

/** Temps de correction opposée après virage (ms) */
#define OPPOSEE 300

#endif
