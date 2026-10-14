/**
 * @file gestionRobot.h
 * @brief Fonctions principales de gestion du robot.
 */
#ifndef GESTION_ROBOT_H
#define GESTION_ROBOT_H

/**
 * @brief Initialise les broches du robot.
 *
 * Configure les capteurs, moteurs, PWM et périphériques.
 */
void setupPin();

/**
 * @brief Arrête immédiatement le robot.
 *
 * Coupe la vitesse des moteurs.
 */
void stop();

/**
 * @brief Gère une intersection selon une instruction donnée.
 *
 * @param instruct Instruction à exécuter :
 * - 0 : Avancer
 * - 1 : Tourner à gauche
 * - 2 : Tourner à droite
 */
void gestionIntersection(int instruct);

/**
 * @brief Assure le suivi de ligne jusqu’à une intersection.
 */
void gestionSuiviLigne();

#endif
