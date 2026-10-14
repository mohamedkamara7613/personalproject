#include "initVarRobot.h"
#include "etatCapteur.h"
#include <wiringPi.h>

EtatCapteur obtenirEtatCapteur(){
    EtatCapteur e;
    
    e.ligneGauche = digitalRead(CAPTEUR_LIGNE_GAUCHE);
    e.ligneDroit = digitalRead(CAPTEUR_LIGNE_DROIT);

    e.intersectionGauche = digitalRead(CAPTEUR_INTERSECTION_GAUCHE);
    e.intersectionDroit = digitalRead(CAPTEUR_INTERSECTION_DROIT);

    return e;
}