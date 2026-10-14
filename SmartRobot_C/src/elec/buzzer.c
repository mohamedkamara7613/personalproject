#include <wiringPi.h>
#include "elec/initVarRobot.h"
#include "elec/buzzer.h"

void buzzer_beep_ms(int duration_ms) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(duration_ms);
    digitalWrite(BUZZER_PIN, LOW);
}
