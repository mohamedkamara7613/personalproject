#ifndef RGB_COLOR_H
#define RGB_COLOR_H

#include <stdint.h>

// Valeurs brutes RGBC lues sur le TCS3472.
struct RgbcValues {
    uint16_t clear;
    uint16_t red;
    uint16_t green;
    uint16_t blue;
};

/**
 * Initialise le capteur de couleur TCS3472 (I2C 0x29) et demarre la premiere conversion.
 * @return 0 en cas de succes, -1 si l'initialisation echoue.
 */
int rgb_color_init(void);

/**
 * Lit les valeurs RGBC courantes (attend au moins un cycle d'integration).
 * @param values pointeur de destination pour les mesures.
 * @return 0 en cas de succes, -1 sinon.
 */
int rgb_color_read(struct RgbcValues *values);

/**
 * Convertit les valeurs brutes en composantes 0-255 normalisees (simple ratio par le canal clair).
 * Les pointeurs r/g/b doivent etre non nuls.
 */
void rgb_color_normalize(const struct RgbcValues *raw, float *r, float *g, float *b);

/**
 * Renvoie le nom de la couleur dominante (R, G, B, Black, White).
 * Retourne "None" si aucune mesure exploitable.
 */
const char *rgb_color_dominant(const struct RgbcValues *raw);

/**
 * Lit le capteur puis affiche la couleur dominante sur le LCD (ligne "Color: <X>").
 * @return 0 si OK, -1 si echec (lecture capteur ou LCD).
 */
int rgb_color_display_on_lcd(void);

// Configuration pour le thread de lecture continue.
struct RgbColorThreadConfig {
    unsigned int delai_ms; // delai entre deux lectures (ms), par defaut 200ms si 0.
};

/**
 * Fonction de thread: boucle de lecture/affichage continu de la couleur.
 * Utilisation: pthread_create(&tid, NULL, rgb_color_thread_loop, &cfg);
 */
void *rgb_color_thread_loop(void *arg);

#endif // RGB_COLOR_H
