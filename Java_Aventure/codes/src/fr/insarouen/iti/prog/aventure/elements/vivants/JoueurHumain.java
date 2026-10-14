package fr.insarouen.iti.prog.aventure.elements.vivants;

import fr.insarouen.iti.prog.aventure.elements.structure.Piece;
import fr.insarouen.iti.prog.aventure.Monde;
import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;
import java.util.Arrays;

import fr.insarouen.iti.prog.aventure.NomDEntiteDejaUtiliseDansLeMondeException;
import fr.insarouen.iti.prog.aventure.elements.structure.ObjetAbsentDeLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.objets.ObjetNonDeplacableException;
import fr.insarouen.iti.prog.aventure.elements.structure.PorteInexistanteDansLaPieceException;
import fr.insarouen.iti.prog.aventure.elements.structure.PorteFermeException;
import fr.insarouen.iti.prog.aventure.ITIAventureException;
import fr.insarouen.iti.prog.aventure.elements.ActivationException;

public class JoueurHumain extends Vivant {

    String ordre = "";

    public JoueurHumain(String nom, Monde monde, int pointsVie, int pointsForce, Piece piece, Objet... objets)
            throws NomDEntiteDejaUtiliseDansLeMondeException {
        super(nom, monde, pointsVie, pointsForce, piece, objets);
    }

    public String getOrdre() {
        return this.ordre;
    }

    public void setOrdre(String ordre) {
        this.ordre = ordre;
    }

    public void executer() throws ITIAventureException {
        // nel'est plus
        // ArrayList<String> arrl = new ArrayList<>();
        // Scanner scanner = new Scanner(this.getOrdre());
        // String nomMethode = "commande" + scanner.next();

        // String param1 = scanner.next();
        // String param2 = "";
        // if(scanner.hasNext("avec")){
        // param2 = scanner.next("avec");
        // param2 = scanner.next();
        // }

        String commande = this.getCommande();
        Object[] parametresEffectifs = this.getParametres();
        Class<String>[] typeParametresFormels = this.getTypesParametresFormels(parametresEffectifs);
        try {
            Method methode = getClass().getDeclaredMethod("commande" + commande, typeParametresFormels);
            methode.invoke(this, parametresEffectifs);
        } catch (InvocationTargetException e) {
            throw (ITIAventureException) e.getCause();
        } catch (Exception e) {
            throw new CommandeImpossiblePourLeVivantException(String.format("impossible d'effectuer la commande"));
        }
    }

    private String getCommande() {
        return ordre.substring(0, ordre.indexOf(" "));

    }

    private Object[] getParametres() {
        return Arrays.stream(ordre.split(" ")).skip(1).filter(s -> !s.equalsIgnoreCase("avec")).toArray();
    }

    private Class<String>[] getTypesParametresFormels(Object[] parametres) {

        Class<String>[] parametresFormels = (Class<String>[]) new Class[parametres.length];
        Arrays.fill(parametresFormels, String.class);
        return parametresFormels;
    }

    private void commandePrendre(String nomObjet) throws ObjetAbsentDeLaPieceException, ObjetNonDeplacableException {
        this.prendre(nomObjet);
    }

    private void commandePoser(String nomObjet) throws ObjetNonPossedeParLeVivantException {
        this.deposer(nomObjet);
    }

    private void commandeFranchir(String nomPorte) throws PorteFermeException, PorteInexistanteDansLaPieceException {
        this.franchir(nomPorte);
    }

    private void commandeOuvrirPorte(String nomPorte) throws ActivationException, PorteInexistanteDansLaPieceException {
        this.getPiece().getPorte(nomPorte).activer();
    }

    private void commandeOuvrirPorte(String nomPorte, String nomObjet)
            throws ActivationException, PorteInexistanteDansLaPieceException, ObjetNonPossedeParLeVivantException {
        Objet obj = this.getObjet(nomObjet);
        this.getPiece().getPorte(nomPorte).activerAvec(obj);
    }
}