#ifndef LCD_DISPLAY_H
#define LCD_DISPLAY_H

/**
 * \file lcd_display.h
 * \brief Affichage de chaînes de caractères sur un écran LCD 16x2 via module I2C PCF8574 (wiringPi/lcd.h).
 * \author Membres du PI Smart Robot 28
 * \version 1.0
 * \date 2025
 */

/**
 * \brief Initialise le LCD (16x2, interface I2C PCF8574).
 * \return 0 en cas de succès, -1 en cas d'échec.
 */
int lcd_display_init(void);

/**
 * \brief Affiche une chaîne sur une ligne du LCD 16x2.
 * \param ligne 0 pour la ligne du haut, 1 pour celle du bas.
 * \param text Chaîne de caractères à afficher (tronquée à 16 caractères), complétée par des espaces.
 * \note Necessite un appel prealable a lcd_display_init().
 */
void afficher_LCD(int ligne, const char *text);

/**
 * \brief Met à jour une ligne sans effacer l'autre (ligne 0: haut, ligne 1: bas).
 *        La ligne est remplie d'espaces au-delà de la chaîne pour effacer d'anciens caractères.
 * \param row 0 ou 1
 * \param text Chaîne à afficher (tronquée à 16 caractères).
 */
void lcd_display_set_line(int row, const char *text);

/**
 * \brief Met à jour les deux lignes en une seule opération.
 * \param line0 Texte ligne 0 (haut), tronqué à 16 caractères.
 * \param line1 Texte ligne 1 (bas), tronqué à 16 caractères.
 */
void lcd_display_set_lines(const char *line0, const char *line1);

#endif // LCD_DISPLAY_H
