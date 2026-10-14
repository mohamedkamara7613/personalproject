#include <unistd.h>
#include <wiringPi.h>
#include <stdbool.h>
#include <stdio.h>


#define CAPTEUR_INTERSECTION_GAUCHE 27
#define CAPTEUR_INTERSECTION_DROIT 22

#define CAPTEUR_LIGNE_GAUCHE 21
#define CAPTEUR_LIGNE_MILIEU 1
#define CAPTEUR_LIGNE_DROIT 5

// ENABLE DES MOTEURS
#define EN1 23
#define EN2 26

// MOTEUR GAUCHE
#define IN1 2
#define IN2 3

// MOTEUR DROIT
#define IN3 6
#define IN4 25

int main(void)

    // wiringPi
    wiringPiSetup();

    // setup enable moteur
    pinMode(EN1, PWM_OUTPUT);
    pinMode(EN2, PWM_OUTPUT);

    // setup moteur gauche droite
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    // vitesseMax
    pwmWrite(EN1, 10.24*VITESSE);
    pwmWrite(EN2, 10.24*VITESSE);

    // moteur gauche droite avance
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);

    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);

    // attend 3 sec
    delay(3000);
    
    // stop
    pwmWrite(EN1, 0);
    pwmWrite(EN2, 0);
}