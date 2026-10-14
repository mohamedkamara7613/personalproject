package fr.insarouen.iti.prog.aventure;

import java.util.Collection;
import java.util.Scanner;
import fr.insarouen.iti.prog.aventure.conditions.EtatDuJeu;
import fr.insarouen.iti.prog.aventure.conditions.ConditionDeFin;
import fr.insarouen.iti.prog.aventure.elements.Entite;
import fr.insarouen.iti.prog.aventure.elements.Executable;
import fr.insarouen.iti.prog.aventure.elements.vivants.JoueurHumain;

public class Simulateur {

    private Monde monde;
    private Collection<ConditionDeFin> conditionsDeFin;
    private Scanner scanner;

    public Simulateur(Monde monde, Collection<ConditionDeFin> conditionsDeFin) {
        this.monde = monde;
        this.conditionsDeFin = conditionsDeFin;
        this.scanner = new Scanner(System.in);
    }

    public EtatDuJeu executerUnTour() {
        for (Entite entite : monde.getEntites()) {
            if (entite instanceof JoueurHumain) {
                JoueurHumain joueur = (JoueurHumain) entite;
                System.out.println(joueur.toString());
                boolean commandeValide = false;

                while (!commandeValide) {
                    System.out.println("\nEntrez votre ordre : ");
                    if (!scanner.hasNextLine())
                        break; // securite
                    String ordre = scanner.nextLine();

                    if (ordre == null || ordre.trim().isEmpty()) {
                        continue;
                    }
                    joueur.setOrdre(ordre.trim());

                    try {
                        joueur.executer();
                        commandeValide = true;
                    } catch (ITIAventureException e) {
                        System.out.println("==> Action impossible : " + e.getMessage());
                    } catch (Exception e) {
                        System.out.println("==> Erreur : commande non reconnue ou invalide (" + e.getMessage() + ")");
                    }
                }
            } else if (entite instanceof Executable) {
                try {
                    System.out.println(entite.toString());
                    ((Executable) entite).executer();
                } catch (ITIAventureException e) {

                    System.out.println("==> Action du Monstre/PNJ impossible : " + e.getMessage());
                }
            }
        }

        EtatDuJeu etatActuel = EtatDuJeu.ENCOURS;
        for (ConditionDeFin cond : conditionsDeFin) {
            EtatDuJeu eval = cond.verifierCondition();
            if (eval != EtatDuJeu.ENCOURS) {
                etatActuel = eval;
            }
        }

        return etatActuel;
    }

    public void executerJusquALaFin() {
        System.out.println("=== DEBUT DE LA SIMULATION ===");
        EtatDuJeu etat = EtatDuJeu.ENCOURS;

        while (etat == EtatDuJeu.ENCOURS) {
            etat = executerUnTour();
        }

        System.out.println("\n=== FIN DE LA PARTIE ===");
        if (etat == EtatDuJeu.SUCCES) {
            System.out.println("VICTOIRE ! Vous avez accompli votre mission !");
        } else if (etat == EtatDuJeu.ECHEC) {
            System.out.println("ECHEC... Vous avez echoue :(");
        }
    }
}