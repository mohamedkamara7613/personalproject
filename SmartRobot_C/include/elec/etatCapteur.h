/**
 * @file etatCapteur.h
 * @brief Définition et accès à l’état des capteurs du robot.
 */
#ifndef ETATCAPTEUR_H
#define ETATCAPTEUR_H

#include <stdbool.h>

/**
 * @brief Structure représentant l’état des capteurs du robot.
 *
 * Chaque champ indique l’état logique (actif/inactif)
 * d’un capteur de ligne ou d’intersection.
 */
typedef struct {
    bool intersectionGauche;
    bool intersectionDroit;
    bool ligneMilieu;
    bool ligneGauche;
    bool ligneDroit;
} EtatCapteur;

/**
 * @brief Lit l’état actuel de tous les capteurs.
 *
 * @return Une structure EtatCapteur remplie.
 */
EtatCapteur obtenirEtatCapteur();

#endif
