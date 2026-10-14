#include <wiringPi.h>
#include <pcf8574.h>
#include <lcd.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "elec/lcd_display.h"

#define AF_BASE 64
#define AF_RS (AF_BASE + 0)
#define AF_RW (AF_BASE + 1)
#define AF_E (AF_BASE + 2)
#define AF_LED (AF_BASE + 3)

#define AF_DB4 (AF_BASE + 4)
#define AF_DB5 (AF_BASE + 5)
#define AF_DB6 (AF_BASE + 6)
#define AF_DB7 (AF_BASE + 7)

#define LCD_COLS 16
#define LCD_ROWS 2

// `sudo i2cdetect -y 1` (to find commonly 0x27 or 0x3F)
#define I2C_ADDR 0x27

static int lcdInitializing = 0;
static int lcdHandle = -1;
static int lcdReady = 0;

static void lcdWriteLine(int row, const char *text) {
    if (row < 0 || row >= LCD_ROWS) {
        return;
    }
    char buf[LCD_COLS];
    for (int i = 0; i < LCD_COLS; i++) {
        buf[i] = ' ';
    }
    if (text != NULL) {
        int len = (int)strlen(text);
        if (len > LCD_COLS) len = LCD_COLS;
        for (int i = 0; i < len; i++) {
            buf[i] = text[i];
        }
    }
    lcdPosition(lcdHandle, 0, row);
    for (int i = 0; i < LCD_COLS; i++) {
        lcdPutchar(lcdHandle, buf[i]);
    }
}

static int setupLcd(void) {
    if (lcdReady || lcdInitializing) {
        return 0;
    }

    lcdInitializing = 1;

    if (pcf8574Setup(AF_BASE, I2C_ADDR) < 0) {
        fprintf(stderr, "pcf8574 setup failed (check I2C address)\n");
	lcdInitializing = 0;
        return -1;
    }

    lcdHandle = lcdInit(LCD_ROWS, LCD_COLS, 4,
                        AF_RS, AF_E,
                        AF_DB4, AF_DB5, AF_DB6, AF_DB7,
                        0, 0, 0, 0);

    if (lcdHandle < 0) {
        fprintf(stderr, "lcdInit failed\n");
	lcdInitializing = 0;
        return -1;
    }

    // Configure backpack pins: LED on, RW held low.
    for (int i = 0; i < 8; i++) {
        pinMode(AF_BASE + i, OUTPUT);
    }
    digitalWrite(AF_LED, 1);
    digitalWrite(AF_RW, 0);

    lcdDisplay(lcdHandle, 1);
    lcdCursor(lcdHandle, 0);
    lcdClear(lcdHandle); // Full clear once at init.
    lcdReady = 1;
    lcdInitializing = 0;
    return 0;
}

int lcd_display_init(void) {
    if (wiringPiSetup() < 0) {
        fprintf(stderr, "wiringPi setup failed\n");
        return -1;
    }
    return setupLcd();
}

void lcd_display_set_lines(const char *line0, const char *line1) {
    if (!lcdReady) {
        if (lcd_display_init() < 0) {
            return;
        }
    }

    // Update both lines, padding with spaces.
    lcdWriteLine(0, line0);
    lcdWriteLine(1, line1);
}

void lcd_display_set_line(int row, const char *text) {
    lcdWriteLine(row, text);
}

void afficher_LCD(int ligne, const char *text) {
    lcd_display_set_line(ligne, text);
}
