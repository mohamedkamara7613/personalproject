#ifndef BUZZER_H
#define BUZZER_H

/**
 * Initialise le buzzer sur la broche GPIO 19 (BCM).
 * @return 0 en cas de succes, -1 sinon.
 */
int buzzer_init(void);

/**
 * Emet un bip pendant la duree indiquee (en millisecondes).
 * @param duration_ms duree du bip.
 */
void buzzer_beep_ms(int duration_ms);

#endif // BUZZER_H
