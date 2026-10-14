/**
 * @file type_def.h
 * @brief Définitions de types génériques du projet partie elec.
 */
#ifndef TYPE_DEF
#define TYPE_DEF

#include <stdbool.h>
#include <stddef.h>
#include "instruction.h"

/**
 * @brief Structure représentant un état partiel des capteurs.
 */
struct EtatCapteur{
    bool intersectionGauche;
    bool intersectionDroit;
    bool ligneGauche;
    bool ligneDroit;
};

/**
 * @brief Retourne l’état actuel des capteurs.
 *
 * @return Structure EtatCapteur.
 */
struct EtatCapteur obtenirEtatCapteur();

/**
 * @brief Tableau d’instructions avec taille associée.
 */
typedef struct {
    const Instruction *data;
    size_t len;
} typeInstructions;

/**
 * @brief Récupère la liste des instructions.
 *
 * @return Structure contenant les instructions.
 */
typeInstructions obtenirInstruction(void);

/**
 * @brief Retourne le nombre d’instructions.
 *
 * @param instructions Structure d’instructions.
 * @return Nombre d’éléments.
 */
size_t longueur(typeInstructions instructions);

#endif
