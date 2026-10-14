package fr.insarouen.iti.prog.sgbd.execution;

import fr.insarouen.iti.prog.sgbd.parseur.SGBDParser;
import fr.insarouen.iti.prog.sgbd.parseur.ParseException;
import fr.insarouen.iti.prog.sgbd.parseur.TokenMgrError;
import fr.insarouen.iti.prog.sgbd.data.EnregistreurSerialisation;
import fr.insarouen.iti.prog.sgbd.data.GestionnaireStockage;
import fr.insarouen.iti.prog.sgbd.data.LecteurSerialisation;
import fr.insarouen.iti.prog.sgbd.modele.BaseDeDonnees;
import java.io.FileInputStream;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.util.Scanner;

public class Interpreteur {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String dossier = "saves/";
        new File(dossier).mkdirs();

        GestionnaireStockage gestionnaire = new GestionnaireStockage(
            new LecteurSerialisation(),
            new EnregistreurSerialisation()
        );

        // Boucle principale : on revient ici apres chaque "menu"
        while (true) {
            BaseDeDonnees bd = null;

            while (bd == null) {
                afficherMenu(dossier);

                System.out.print("Ton choix : ");
                String choix = sc.nextLine().trim();

                if (choix.equals("1")) {
                    String nom = "";
                    while (nom.isEmpty()) {
                        System.out.print("Nom de la nouvelle base : ");
                        nom = sc.nextLine().trim();
                        if (nom.isEmpty()) {
                            System.out.println("[ERREUR] Le nom ne peut pas être vide.");
                        }
                    }
                                        
                    String chemin = dossier + nom + ".ser";

                    if (GestionnaireStockage.baseExiste(chemin)) {
                        System.out.println("[ERREUR] Une base '" + nom + "' existe deja.");
                        pause(sc);
                        continue;
                    }
                    try {
                        bd = new BaseDeDonnees(nom);
                        gestionnaire.sauvegarder(bd, chemin);
                        System.out.println("Base '" + nom + "' creee.");
                    } catch (Exception e) {
                        System.out.println("[ERREUR] " + e.getMessage());
                        pause(sc);
                    }

                } else if (choix.equals("2")) {
                    System.out.print("Nom de la base a charger : ");
                    String nom = sc.nextLine().trim();
                    String chemin = dossier + nom + ".ser";

                    if (!GestionnaireStockage.baseExiste(chemin)) {
                        System.out.println("[ERREUR] Aucune base '" + nom + "' trouvee.");
                        pause(sc);
                        continue;
                    }
                    try {
                        bd = gestionnaire.charger(chemin);
                        System.out.println("Base '" + nom + "' chargee.");
                    } catch (Exception e) {
                        System.out.println("[ERREUR] " + e.getMessage());
                        pause(sc);
                    }

                } else if (choix.equals("3")) {
                    afficherBasesExistantes(dossier);
                    pause(sc);

                } else if (choix.equals("4")) {
                    System.out.println("Au revoir ;)");
                    System.exit(0);
                }
            }

            // On a une base - on lance l'interpreteur
            if (args.length == 0) {
                interpreteurConsole(bd, gestionnaire, dossier + bd.getNom() + ".ser", sc);
            } else {
                interpreteurFichier(args[0], bd, gestionnaire, dossier + bd.getNom() + ".ser");
                interpreteurConsole(bd, gestionnaire, dossier + bd.getNom() + ".ser", sc);
            }
            // interpreteurConsole a retourne -> "menu" tape -> on reboucle
        }
    }

    // -------------------------------------------------------------------------

    private static void afficherMenu(String dossier) {
        System.out.print("\033[H\033[2J");
        System.out.flush();

        System.out.println();
        System.out.println("          +----------------------------------+");
        System.out.println("          |         MINI-SGBD - ACCUEIL      |");
        System.out.println("          +----------------------------------+");

        File[] fichiers = new File(dossier).listFiles(f -> f.getName().endsWith(".ser"));
        if (fichiers != null && fichiers.length > 0) {
            System.out.println("          |  Bases disponibles :             |");
            for (File f : fichiers) {
                String nom = f.getName().replace(".ser", "");
                System.out.printf("          |    - %-28s|%n", nom);
            }
            System.out.println("          +----------------------------------+");
        }

        System.out.println("          |  1 - Creer une nouvelle base     |");
        System.out.println("          |  2 - Charger une base existante  |");
        System.out.println("          |  3 - Afficher les bases          |");
        System.out.println("          |  4 - Quitter                     |");
        System.out.println("          +----------------------------------+");
        System.out.println();
    }

    private static void afficherBasesExistantes(String dossier) {
        File[] fichiers = new File(dossier).listFiles(f -> f.getName().endsWith(".ser"));
        System.out.println();
        System.out.println("          +----------------------------------+");
        System.out.println("          |        BASES EXISTANTES          |");
        System.out.println("          +----------------------------------+");
        if (fichiers == null || fichiers.length == 0) {
            System.out.println("          |  (aucune base sauvegardee)       |");
        } else {
            for (File f : fichiers) {
                String nom = f.getName().replace(".ser", "");
                System.out.printf("          |    - %-28s|%n", nom);
            }
        }
        System.out.println("          +----------------------------------+");
    }

    private static void pause(Scanner sc) {
        System.out.print("\nAppuyez sur Entree pour continuer...");
        sc.nextLine();
    }

    // -------------------------------------------------------------------------

    public static void interpreteurConsole(BaseDeDonnees db, GestionnaireStockage gestionnaire, String chemin, Scanner sc) {
        System.out.println("\nBase '" + db.getNom() + "' active. Tapez 'menu' pour revenir au menu.\n");
        System.out.print("sgbd> ");

        String commande = "";
        try {
            while (true) {
                String ligne = sc.nextLine();
                commande += ligne;

                String commandeLower = commande.trim().toLowerCase();
                String commandeTrim  = commande.trim();
                
                if (commandeLower.equals("menu") || commandeLower.equals("menu;")) {
                    System.out.println("Retour au menu principal...\n");
                    return;
                }

                if (commandeLower.equals("quit") || commandeLower.equals("exit") ||
                    commandeLower.equals("quit;") || commandeLower.equals("exit;")) {
                    System.out.println("Au revoir ;)");
                    System.exit(0);
                }

                if(commandeLower.startsWith("source ")){
                    String cheminFichier = commandeTrim.substring(7).trim();
                    cheminFichier = cheminFichier.substring(0, cheminFichier.length() - 1).trim();
                  

                    if (cheminFichier.isEmpty()){
                        System.out.println("[ERREUR] Syntaxe : source <chemin_vers_fichier.sql>"); 
                    } else {
                        System.out.println("Execution du fichier : " + cheminFichier);
                        interpreteurFichier(cheminFichier, db, gestionnaire, chemin);
                    }

                    commande = "";
                    System.out.print("sgbd> ");
                }


                if (commande.trim().endsWith(";")) {
                    commande = commande.trim();

                    byte[] bytes = commande.getBytes();
                    ByteArrayInputStream bais = new ByteArrayInputStream(bytes);
                    SGBDParser parser = new SGBDParser(bais);
                    parser.setDatabase(db);

                    try {
                        parser.Commande();
                        gestionnaire.sauvegarder(db, chemin);
                    } catch (ParseException e) {
                        System.out.println("[ERREUR] Syntaxe incorrecte : " + e.getMessage());
                    } catch (TokenMgrError e) {
                        System.out.println("[ERREUR] Caractere inconnu : " + e.getMessage());
                    } catch (RuntimeException e) {
                        System.out.println("[ERREUR] " + e.getMessage());
                    } catch (Exception e) {
                        System.out.println("[ERREUR FATALE] " + e.getMessage());
                    }

                    commande = "";
                    System.out.print("sgbd> ");
                    continue; 
                }
            }
        } catch (java.util.NoSuchElementException e) {
            System.out.println("\nAu revoir ;)");
        }
    }

    public static void interpreteurFichier(String cheminFichier, BaseDeDonnees db, GestionnaireStockage gestionnaire, String chemin) {
        try {
            FileInputStream fis = new FileInputStream(cheminFichier);
            SGBDParser parser = new SGBDParser(fis);
            parser.setDatabase(db);
            System.out.println("Analyse du fichier : " + cheminFichier);

            while (true) {
                try {
                    parser.Commande();
                } catch (ParseException e) {
                    if (e.getMessage() != null && e.getMessage().contains("EOF")) break;
                    System.out.println("[ERREUR] " + e.getMessage());
                    break;
                } catch (TokenMgrError e) {
                    System.out.println("[ERREUR] " + e.getMessage());
                    break;
                }
            }
        } catch (java.io.FileNotFoundException e) {
            System.out.println("[ERREUR] Fichier introuvable : " + cheminFichier);
        } catch (Exception e) {
            System.out.println("[ERREUR] Lecture : " + e.getMessage());
        }
    }
}