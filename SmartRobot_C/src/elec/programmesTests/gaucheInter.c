#include <unistd.h>
#include <wiringPi.h>
#include <stdbool.h>
#include <stdio.h>


#define CAPTEUR_INTERSECTION_GAUCHE 27
#define CAPTEUR_INTERSECTION_DROIT 22

#define CAPTEUR_LIGNE_GAUCHE 21
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

struct EtatCapteur{
    bool intersectionGauche;
    bool intersectionDroit;
    bool ligneGauche;
    bool ligneDroit;
};

struct EtatCapteur obtenirEtatCapteur(){
    struct EtatCapteur e;
    e.ligneGauche = digitalRead(CAPTEUR_LIGNE_GAUCHE);
    e.ligneDroit = digitalRead(CAPTEUR_LIGNE_DROIT);
    
    e.intersectionGauche = digitalRead(CAPTEUR_INTERSECTION_GAUCHE);
    e.intersectionDroit = digitalRead(CAPTEUR_INTERSECTION_DROIT);

    return e;
}

int main(void){
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

    // setup capteur ligne
    pinMode(CAPTEUR_LIGNE_GAUCHE, INPUT);
    pinMode(CAPTEUR_LIGNE_DROIT, INPUT);
    pinMode(CAPTEUR_INTERSECTION_GAUCHE, INPUT);
    pinMode(CAPTEUR_INTERSECTION_DROIT, INPUT);

    struct EtatCapteur etatCapteur;
    etatCapteur = obtenirEtatCapteur();
    bool surLigne = (etatCapteur.ligneGauche && etatCapteur.ligneDroit);

    // vitesseMax
    pwmWrite(EN1, 10.24*VITESSE);
    pwmWrite(EN2, 10.24*VITESSE);

    // tourne gauche
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
            
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);

    etatCapteur = obtenirEtatCapteur();

    while (surLigne){
        etatCapteur = obtenirEtatCapteur();
        surLigne = (etatCapteur.ligneGauche && etatCapteur.ligneDroit);
    }

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
            
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
    delay(500)

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
            
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    while(!surLigne){
        etatCapteur = obtenirEtatCapteur();
        surLigne = (etatCapteur.ligneGauche && etatCapteur.ligneDroit);
    }

    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
            
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);

    // stop après 3 sec (3000 * 1 ms)
    pwmWrite(EN1, 0);
    pwmWrite(EN2, 0);
}