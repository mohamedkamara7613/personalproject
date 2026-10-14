# Compte Rendu - Programmation Orientée Objet - TP08 (Aventure)

Ce document valide et résume l'ensemble des accomplissements réalisés au cours du TP08, visant à finaliser le jeu d'aventure interactif. Le projet tourne désormais de façon autonome grâce au moteur de simulation.

## 1. Conditions de fin et Moteur d'évaluation
Les fonctionnalités liées à la gestion des conditions de l'environnement permettant d'évaluer la victoire ou la défaite sont achevées :
- Définition et utilisation de l'énumération `EtatDuJeu` (`ENCOURS`, `SUCCES`, `ECHEC`).
- Adaptation des Lecteurs (descriptions textuelles et fichiers sérialisés) pour capturer les conditions de fin.
- Toutes les classes héritant de `ConditionDeFin` ont été corrigées pour renvoyer dynamiquement l'état attendu (`this.getEtatSiConditonVerifiee()`) via le polymorphisme. Les problèmes de *shadowing* et la gestion de la nullité ont été résolus.

## 2. Intelligence du Joueur et Réflexion
La classe `JoueurHumain` est désormais capable de parser du vocabulaire naturel (ex: `"OuvrirPorte Porte42"`).
- L'API de *Reflection* trouve dynamiquement les méthodes correspondant à la commande saisie.
- Exécution de type `methode.invoke(...)` avec traitement rigoureux des `InvocationTargetException` reconverties en exceptions du domaine de l'application (comme `ObjetAbsentDeLaPieceException`).

## 3. Classe `Simulateur` et Interfaces 
La pierre angulaire du jeu qui chapeaute tout l'espace textuel :
- Tous les protagonistes d'actions, comme `Vivant` (et donc `Monstre` ou `JoueurHumain`), implémentent formellement ou explicitement l'interface `Executable`.
- `executerUnTour()` itère de manière fluide sur toutes les entités de l'univers, interrogeant continuellement les utilisateurs via un flux `Scanner` standard si des blocages d'exécution (erreurs de saisie ou interdiction physique) se présentent.
- `executerJusquALaFin()` a été impliqué pour boucler tant que la condition de victoire ou d'échec du monde n'a pas été déclenchée.

## 4. Architecture Globale
Le point d'entrée historique du jeu a été mis de côté pour intégrer la version complète de `Main.java` fournie, qui gère automatiquement un menu proposant de charger, sauver, ou itérer un/des tours du simulateur en direct.

---

# Extensions Facultatives (Démonstrations Théoriques)

*Afin de prouver la compréhension des notions bonus proposées par le sujet, voici les implémentations proposées pour les exercices facultatifs. Par choix de simplicité pour le projet actuel, ces propositions ne sont pas intégrées dans les fichiers sources .*

### 1. Factorisation via `ConjonctionConditionDeFin` (Varargs)
Plutôt que d'écrire de multiples conditions combinées "en dur", la conception orientée objet incite à utiliser un conteneur variadique pour agglomérer une série infinie de petites conditions atomiques.

```java
package fr.insarouen.iti.prog.aventure.conditions;

import java.util.Arrays;
import java.util.Collection;

public class ConjonctionConditionDeFin extends ConditionDeFin {
    
    private Collection<ConditionDeFin> conditions;

    public ConjonctionConditionDeFin(EtatDuJeu etat, ConditionDeFin... conditions) {
        super(etat);
        // Le paramètre "conditions" est un tableau implicite (varargs)
        this.conditions = Arrays.asList(conditions);
    }

    @Override
    public EtatDuJeu verifierCondition() {
        for (ConditionDeFin cond : conditions) {
            // Si l'une des sous-conditions n'est pas atteinte :
            if (cond.verifierCondition() != this.getEtatSiConditonVerifiee()) {
                return EtatDuJeu.ENCOURS;
            }
        }
        // Toutes les conditions sont remplies
        return this.getEtatSiConditonVerifiee();
    }
}
```

### 2. Optimisation du Filtrage avec l'API *Streams*
Plutôt que de tester manuellement via `instanceof JoueurHumain` dans une boucle ou de dupliquer la méthode de filtre, l'utilisation couplée de la généricité Java `<T>` et des **Streams** permet de factoriser de façon propre l'extraction.

```java
import java.util.stream.Collectors;
import java.util.Collection;

// ... dans la classe Simulateur ...

    /**
     * Méthode générique permettant d'extraire n'importe quelle famille d'entités du monde.
     * Exemple d'appel : getEntites(JoueurHumain.class) ou getEntites(Executable.class)
     */
    private <T> Collection<T> getEntites(Class<T> classe) {
        return this.monde.getEntites().stream()
            .filter(classe::isInstance) // Ne garde que les objets du type désiré
            .map(classe::cast)          // Effectue le polymorphisme / Cast
            .collect(Collectors.toList());
    }
```
Grâce à cela, la méthode `executerUnTour()` pourrait faire `for(JoueurHumain j : getEntites(JoueurHumain.class))` et `for(Executable e : getEntites(Executable.class))`.
