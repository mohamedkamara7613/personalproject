#include <stdbool.h>
#include <unistd.h>
#include <wiringPi.h>
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

#define VITESSE 80
#define DELAIS_INTERSECTION (100 * 1000)

struct EtatCapteur{
    bool intersectionGauche;
    bool intersectionDroit;
    bool ligneGauche;
    bool ligneMilieu;
    bool ligneDroit;
};

struct EtatCapteur obtenirEtatCapteur(){
    struct EtatCapteur e;
    //e.intersectionGauche = digitalRead(CAPTEUR_INTERSECTION_GAUCHE);
    //e.intersectionDroit = digitalRead(CAPTEUR_INTERSECTION_DROIT);
    e.ligneGauche = digitalRead(CAPTEUR_LIGNE_GAUCHE);
    e.ligneMilieu = digitalRead(CAPTEUR_LIGNE_MILIEU);
    e.ligneDroit = digitalRead(CAPTEUR_LIGNE_DROIT);

    e.intersectionGauche = digitalRead(CAPTEUR_INTERSECTION_GAUCHE);
    e.intersectionDroit = digitalRead(CAPTEUR_INTERSECTION_DROIT);

    return e;
}

void avance(){
    pwmWrite(EN1, 10.24*VITESSE);
    pwmWrite(EN2, 10.24*VITESSE);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
}

void gauche(){
    pwmWrite(EN1, 10.24*(VITESSE / 2));
    pwmWrite(EN2, 10.24*(VITESSE / 2 ));
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
//  digitalWrite(IN2, LOW);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
}

void droite(){
    pwmWrite(EN1, 10.24*(VITESSE / 2));
    pwmWrite(EN2, 10.24*(VITESSE / 2 ));
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
//        digitalWrite(IN4, LOW);
}

void stop(){
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, LOW);
}

void stopFrein(){
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, HIGH);
}

struct EtatCapteur etatCapteur;

bool surLigne(){
    etatCapteur = obtenirEtatCapteur();
    return (etatCapteur.ligneMilieu);
}

bool surIntersection(){
    etatCapteur = obtenirEtatCapteur();
    return (etatCapteur.intersectionGauche || etatCapteur.intersectionDroit);
}

void gaucheIntersection(int delais){
    gauche();
    usleep(delais);

    while(!surLigne()){
        usleep(0);
    }
    stop();
}

void droiteIntersection(int delais){
    droite();
    usleep(delais);

    while(!surLigne()){
        usleep(0);
    }
    stop();
}

void tournerIntersection(int delais, int direction){
    if (direction == 0){
        gauche();
    } else {
        droite();
    }
    etatCapteur = obtenirEtatCapteur();
    while (etatCapteur.ligneGauche || etatCapteur.ligneDroit){
        usleep(0);
        etatCapteur = obtenirEtatCapteur();
    }
    if (direction == 0){
        gaucheIntersection(delais);
    } else {
        droiteIntersection(delais);
    }
    stop();
}

void suivreLigne(int delais){
    etatCapteur = obtenirEtatCapteur();
    usleep(0);
    //printf("Status : %d %d",etatCapteur.ligneGauche, etatCapteur.ligneDroit);

    /*if ((!etatCapteur.ligneGauche) && (!surLigne())){
        droiteIntersection(0);
    }
    else if (!etatCapteur.ligneDroit){
            gaucheIntersection(0);
    }*/
    if ((!etatCapteur.ligneGauche && etatCapteur.ligneDroit) || (!etatCapteur.ligneDroit && etatCapteur.ligneGauche)){
        if (!etatCapteur.ligneGauche){
            printf("entree droite");
            droiteIntersection(0);
            printf("sortie droite");
        }
        else if (!etatCapteur.ligneDroit){
            printf("entree gauche");
            gaucheIntersection(0);
            printf("sortie gauche");
        }
    } else {
        avance();
        printf("j'avance");
    }
    printf("ma mère c'est une gentille personne\n");
}

void avanceIntersection(int delais){
    //avance();
    stop();
    usleep(delais);

    struct EtatCapteur etatCapteur;
    etatCapteur = obtenirEtatCapteur();
    bool inter = false;
    bool ancierInter = false;
    while (!inter){
        //printf('Status : %d %d\n', etatCapteur.intersectionGauche, etatCapteur.intersectionDroit);
        printf("entree suivreLigne\n");
        suivreLigne(50 * 1000);
        printf("Sortie suivreLigne\n");

        etatCapteur = obtenirEtatCapteur();

        if (!(inter = ancierInter)){
            printf("status : %d %d ", etatCapteur.intersectionGauche, etatCapteur.intersectionDroit);
        }
        else {
            ancierInter = inter;
        }

        inter = (etatCapteur.intersectionGauche || etatCapteur.intersectionDroit);

        
    }

    stop();
}

/*void gererIntersection(int indice, Instructions instructions){
    switch (instructions[indice]){
        case "AV":
            avanceIntersection(DELAIS_INTERSECTION);
            break;
        case "TG":
            gaucheIntersection(DELAIS_INTERSECTION);
            break;
        case "TD":
            droiteIntersection(DELAIS_INTERSECTION);
            break;
    }
}*/

void setupPin() {
    wiringPiSetup();
    pinMode(CAPTEUR_LIGNE_GAUCHE, INPUT);
    pinMode(CAPTEUR_LIGNE_DROIT, INPUT);
    pinMode(EN1, PWM_OUTPUT);
    pinMode(EN2, PWM_OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    //pinMode(CAPTEUR_INTERSECTION_GAUCHE, INPUT);
    //pinMode(CAPTEUR_INTERSECTION_DROIT, INPUT);

    pwmWrite(EN1, 10.24*VITESSE);
    pwmWrite(EN2, 10.24*VITESSE);
//    digitalWrite(EN1, HIGH);
//    digitalWrite(EN2, HIGH);
}

void coupure(){
    pwmWrite(EN1, 0);
    pwmWrite(EN2, 0);
}

int main(void){
    struct EtatCapteur etatCapteur;
//    typeInstructions instructions = obtenirInstruction;

    setupPin();
    stop();
    /*for (int i = 0; i < 3000; i++){
        //gauche();
//        etatCapteur = obtenirEtatCapteur();
//        printf("Status capteurs : %d%d\n", etatCapteur.ligneGauche, etatCapteu                          r.ligneDroit);
        suivreLigne();
//f        gauche();
        printf("Etape prog : %d\n",i);
        delay(2);
        //stop();
        //delay(200)
    }*/

    /*while (true){
        etatCapteur = obtenirEtatCapteur();
        printf("---------\n");
        printf("status : %d %d\n", etatCapteur.ligneGauche, etatCapteur.ligneDroit);
        printf("status : %d %d\n", etatCapteur.intersectionGauche, etatCapteur.intersectionDroit);

        delay(500);
    }*/
    
    avance();
    //avanceIntersection(0);
    /*printf("Check1\n");
    tournerIntersection(300, 1);
    printf("Check2\n");
    avanceIntersection(0);
    printf("Check3\n");
    tournerIntersection(0, 0);
    printf("Check4\n");
    avanceIntersection(0);
    printf("Check5\n");
    tournerIntersection(0, 0);*/
    usleep(1000000*3);
    printf("fin\n");
    stop();
    coupure();
    /*for (int indiceInstructions = 0 ; indiceInstructions < longueur(instructio                          ns) ; indiceInstructions++){
        etatCapteur = obtenirEtatCapteur();
        bool intersection = (etatCapteur.intersectionDroit || etatCapteur.inters                          ectionGauche);

        while(!intersection){
            suivreLigne();
            etatCapteur = obtenirEtatCapteur();
            bool intersection = (etatCapteur.intersectionDroit || etatCapteur.in                          tersectionGauche);
        }
        gererIntersection(indiceInstructions, instructions);
    }*/
}
