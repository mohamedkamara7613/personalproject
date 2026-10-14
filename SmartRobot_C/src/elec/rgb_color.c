#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <unistd.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>
#include <pthread.h>
#include "elec/rgb_color.h"
#include "elec/lcd_display.h"
#include "elec/buzzer.h"


#define TCS3472_ADDR 0x29
#define CMD_BIT 0x80

#define REG_ENABLE 0x00
#define REG_ATIME 0x01
#define REG_CONTROL 0x0F
#define REG_ID 0x12
#define REG_STATUS 0x13
#define REG_CDATAL 0x14
#define REG_RDATAL 0x16
#define REG_GDATAL 0x18
#define REG_BDATAL 0x1A

#define ENABLE_PON 0x01
#define ENABLE_AEN 0x02

// ATIME: (256 - ATIME) * 2.4ms -> ~100ms ici pour limiter le bruit sans saturer.
#define DEFAULT_ATIME 0xD5
// Gain 4x (0x00:1x, 0x01:4x, 0x02:16x, 0x03:60x).
#define DEFAULT_GAIN 0x01

#define CMD(reg) (CMD_BIT | (reg))

// Heuristiques pour classification des couleurs.
#define BLACK_CLEAR_THRESHOLD 120         // Clear brut (16 bits, ~100ms integ) trop faible -> noir.
// Seuils suivants exprimes sur les composantes R/G/B normalisees (0-255).
#define WHITE_MEAN_THRESHOLD 215.0f       // Moyenne des canaux assez haute (blanc).
#define WHITE_BALANCE_TOLERANCE 0.12f     // Ecart relatif max pour etre considere blanc.
#define COLOR_DOM_RATIO 1.4f              // Rapport dominant vs autres (filtre ambiance).
#define COLOR_DOM_DELTA 25.0f             // Ecart minimal en valeur absolue.
#define COLOR_MIN_LEVEL 70.0f             // Niveau minimal pour considerer une couleur.
#define GREEN_STRICT_RATIO 1.6f           // Ratio specifique pour valider un vrai vert.
#define GREEN_STRICT_DELTA 35.0f          // Delta specifique vert vs seconde composante.
#define SATURATION_MIN 0.20f              // Saturation mini (max-min)/max pour accepter une couleur.

static int i2c_fd = -1;
static unsigned int integration_wait_ms = 0;

static unsigned int compute_integration_ms(unsigned char atime) {
    // Datasheet: T_int_ms = (256 - ATIME) * 2.4ms.
    double ms = (256.0 - (double)atime) * 2.4;
    if (ms < 1.0) {
        ms = 1.0;
    }
    return (unsigned int)(ms + 0.5);
}

static int write_reg8(unsigned char reg, unsigned char value) {
    if (i2c_fd < 0) {
        return -1;
    }
    return wiringPiI2CWriteReg8(i2c_fd, CMD(reg), value);
}

static int read_reg8(unsigned char reg) {
    if (i2c_fd < 0) {
        return -1;
    }
    return wiringPiI2CReadReg8(i2c_fd, CMD(reg));
}

static int read_reg16(unsigned char reg, uint16_t *out) {
    if (out == NULL) {
        return -1;
    }
    int low = read_reg8(reg);
    int high = read_reg8(reg + 1);
    if (low < 0 || high < 0) {
        return -1;
    }
    *out = (uint16_t)((high << 8) | low);
    return 0;
}

static int enable_sensor(void) {
    if (write_reg8(REG_ENABLE, ENABLE_PON) < 0) {
        return -1;
    }
    delay(3);
    if (write_reg8(REG_ENABLE, ENABLE_PON | ENABLE_AEN) < 0) {
        return -1;
    }
    delay(integration_wait_ms);
    return 0;
}

static int ensure_ready(void) {
    if (i2c_fd >= 0) {
        return 0;
    }

    if (wiringPiSetup() < 0) {
        fprintf(stderr, "wiringPi setup failed\n");
        return -1;
    }

    i2c_fd = wiringPiI2CSetup(TCS3472_ADDR);
    if (i2c_fd < 0) {
        fprintf(stderr, "I2C setup failed on address 0x%02X\n", TCS3472_ADDR);
        return -1;
    }

    int id = read_reg8(REG_ID);
    if (id < 0) {
        fprintf(stderr, "TCS3472 ID read failed\n");
        return -1;
    }
    if (id != 0x44 && id != 0x4D) {
        fprintf(stderr, "Unexpected TCS3472 ID: 0x%02X (expected 0x44/0x4D)\n", id);
    }

    integration_wait_ms = compute_integration_ms(DEFAULT_ATIME);

    if (write_reg8(REG_ATIME, DEFAULT_ATIME) < 0) {
        return -1;
    }
    if (write_reg8(REG_CONTROL, DEFAULT_GAIN) < 0) {
        return -1;
    }
    return enable_sensor();
}

int rgb_color_init(void) {
    return ensure_ready();
}

int rgb_color_read(struct RgbcValues *values) {
    if (values == NULL) {
        return -1;
    }
    if (ensure_ready() < 0) {
        return -1;
    }

    delay(integration_wait_ms);

    int status = read_reg8(REG_STATUS);
    if (status < 0) {
        return -1;
    }
    if ((status & 0x01) == 0) {
        delay(integration_wait_ms);
    }

    if (read_reg16(REG_CDATAL, &values->clear) < 0) {
        return -1;
    }
    if (read_reg16(REG_RDATAL, &values->red) < 0) {
        return -1;
    }
    if (read_reg16(REG_GDATAL, &values->green) < 0) {
        return -1;
    }
    if (read_reg16(REG_BDATAL, &values->blue) < 0) {
        return -1;
    }

    return 0;
}

void rgb_color_normalize(const struct RgbcValues *raw, float *r, float *g, float *b) {
    if (raw == NULL || r == NULL || g == NULL || b == NULL) {
        return;
    }
    if (raw->clear == 0) {
        *r = 0.0f;
        *g = 0.0f;
        *b = 0.0f;
        return;
    }

    float scale = 255.0f / (float)raw->clear;
    *r = raw->red * scale;
    *g = raw->green * scale;
    *b = raw->blue * scale;

    if (*r > 255.0f) *r = 255.0f;
    if (*g > 255.0f) *g = 255.0f;
    if (*b > 255.0f) *b = 255.0f;
}

const char *rgb_color_dominant(const struct RgbcValues *raw) {
    if (raw == NULL || raw->clear == 0) {
        return "None";
    }

    if (raw->clear < BLACK_CLEAR_THRESHOLD) {
        return "Noir";
    }

    float r, g, b;
    rgb_color_normalize(raw, &r, &g, &b);

    float mean = (r + g + b) / 3.0f;
    float maxc = r;
    if (g > maxc) maxc = g;
    if (b > maxc) maxc = b;
    float minc = r;
    if (g < minc) minc = g;
    if (b < minc) minc = b;

    float diffR = (r > mean) ? (r - mean) : (mean - r);
    float diffG = (g > mean) ? (g - mean) : (mean - g);
    float diffB = (b > mean) ? (b - mean) : (mean - b);
    float maxDiff = diffR;
    if (diffG > maxDiff) maxDiff = diffG;
    if (diffB > maxDiff) maxDiff = diffB;

    // Blanc: canaux balances et moyens eleves.
    if (mean > WHITE_MEAN_THRESHOLD && maxDiff <= WHITE_BALANCE_TOLERANCE * mean) {
        return "Blanc";
    }

    // Saturation insuffisante => aucune couleur saillante.
    float saturation = (maxc > 0.0f) ? ((maxc - minc) / maxc) : 0.0f;
    if (saturation < SATURATION_MIN) {
        return "None";
    }

    if (maxc < COLOR_MIN_LEVEL) {
        return "None";
    }

    // Couleur dominante avec conditions strictes.
    float second = (maxc == r) ? (g > b ? g : b) : (maxc == g ? (r > b ? r : b) : (r > g ? r : g));
    if (maxc < second * COLOR_DOM_RATIO) {
        return "None";
    }
    if ((maxc - second) < COLOR_DOM_DELTA) {
        return "None";
    }

    // Pour le vert, filtre plus strict pour eviter les faux positifs ambiants.
    if (maxc == g) {
        if (g < second * GREEN_STRICT_RATIO) {
            return "None";
        }
        if ((g - second) < GREEN_STRICT_DELTA) {
            return "None";
        }
        return "Vert";
    }

    if (maxc == r) return "Rouge";
    return "Bleu";
}

int rgb_color_display_on_lcd(void) {
    struct RgbcValues v;
    if (rgb_color_read(&v) < 0) {
        return -1;
    }
    const char *label = rgb_color_dominant(&v);

    if (strcmp(label, "Vert") == 0 || strcmp(label, "Rouge") == 0) {

	if (strcmp(label, "Vert") == 0){
		afficher_LCD(0,NULL);
		afficher_LCD(0,"Vert");
	}else{
	    if (strcmp(label, "Rouge") == 0){
            afficher_LCD(0,NULL);
            afficher_LCD(0,"Rouge");
	    }
	}
    buzzer_beep_ms(100);
	delay(300);
	printf("beep \n");
    }
    return 0;
}

void *rgb_color_thread_loop(void *arg) {
    struct RgbColorThreadConfig *cfg = (struct RgbColorThreadConfig *)arg;
    unsigned int delai = (cfg != NULL && cfg->delai_ms > 0) ? cfg->delai_ms : 200;

    if (rgb_color_init() < 0) {
        fprintf(stderr, "Init capteur couleur echouee dans le thread\n");
    }

    while(1) {
        rgb_color_display_on_lcd();
        delay(delai);
    }

    return NULL;
}
