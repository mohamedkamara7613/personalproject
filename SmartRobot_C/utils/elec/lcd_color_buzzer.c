#include <stdio.h>
#include <stdio.h>
#include <string.h>
#include <wiringPi.h>

#include "elec/rgb_color.h"
#include "elec/lcd_display.h"
#include "elec/buzzer.h"

// gcc programmes/tests/elec/lcd_color_buzzer.c programmes/src/elec/rgb_color.c programmes/src/elec/lcd_display.c programmes/src/elec/buzzer.c -Iprogrammes/include -lwiringPi -lwiringPiDev -o programmes/tests/elec/lcd_color_buzzer_demo
// ./programmes/tests/elec/lcd_color_buzzer_demo

int main(void) {
    if (rgb_color_init() < 0) {
        fprintf(stderr, "Init TCS3472 echouee\n");
        return 1;
    }

    int lcd_ok = (lcd_display_init() == 0);
    if (!lcd_ok) {
        fprintf(stderr, "LCD indisponible, poursuite en console\n");
    }
    int buzzer_ok = (buzzer_init() == 0);

    for (int i = 0; i < 30; i++) {
        struct RgbcValues v;
        if (rgb_color_read(&v) < 0) {
            fprintf(stderr, "Lecture capteur echouee\n");
            return 1;
        }

        float r, g, b;
        rgb_color_normalize(&v, &r, &g, &b);
        const char *dom = rgb_color_dominant(&v);

        printf("R/G/B = %6.1f %6.1f %6.1f | Dominante: %s\n", r, g, b, dom);

        if (lcd_ok) {
            char line[17];
            snprintf(line, sizeof(line), "Color: %s", dom);
            afficher_LCD(0, line);
        }

        if (buzzer_ok && (strcmp(dom, "Vert") == 0 || strcmp(dom, "Green") == 0)) {
            buzzer_beep_ms(100);
        }

        delay(200);
    }
    return 0;
}
