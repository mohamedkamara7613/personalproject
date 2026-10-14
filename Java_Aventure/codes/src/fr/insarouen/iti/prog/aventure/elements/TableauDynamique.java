package fr.insarouen.iti.prog.aventure.elements;

import fr.insarouen.iti.prog.aventure.elements.objets.Objet;
import fr.insarouen.iti.prog.aventure.elements.vivants.Vivant;


/**
 * Classe representant un tableau dynamique d'entites.
 */
public class TableauDynamique {
	
	/**
	* Tableau stockant les Entite
	*/
	private Entite[] tab;
	
	/**
	* <p> Constructeur du Tableau Dynamique, initialise le tableau vide.
	* </p>
 	*/
	public TableauDynamique() {
		this.tab = new Entite[0];
	}
	
	/**
	* <p> Crée une copie de tableau d'Entite en itérant tant que possible
	* selon les tailles des tableaux
	* </p>
	* @param source tableau d'entités à copier
	* @param dest tableau d'entités où faire la copie
	* @param i indice du tableau source à partir duquel copier
	* @param j indice du tableau à partir duquel mettre la copie
	* @param n nombre de valeurs à copier
 	*/
	private void copie(Entite[] source, Entite[] dest,int i,int j,int n) {
		
		while (j<dest.length && i<source.length && n>0) {
			dest[j] = source[i];
			i++;
			j++;
			n--;
		}
	}
	/**
	* <p> Ajoute une entité au tableau
	* </p>
	* @param o Entite à ajouter au tableau
 	*/
	public void ajouter(Entite o) {
		Entite[] temp;
		temp = new Entite[this.tab.length + 1];
		if (this.tab.length > 0) {
			copie(this.tab, temp, 0, 0, this.tab.length);
		}
		temp[this.tab.length] = o;
		this.tab = temp;
	}
	
	/**
	* <p> Renvoit l'entité d'indice i
	* </p>
	* @param i l'indice de l'entité recherchée
	* @return l'entité d'indice i
 	*/
	public Entite get(int i) throws ArrayIndexOutOfBoundsException {
		return this.tab[i];
	}

	private int indice(String nom) {

		if (this.tab.length == 0) {
			return -1;
		}

		int i = 0;
		while (i < this.tab.length) {
			if (nom.equals(this.tab[i].getNom())) {
				return i;
			}
			i++;
		}
		return -1;
	}

	private int indice(Entite o) {

		if (this.tab.length == 0) {
			return -1;
		}

		int i = 0;
		while (i < this.tab.length) {
			if (o.equals(this.tab[i])) {
				return i;
			}
			i++;
		}
		return -1;
	}

	/**
	 * Recupere une entite par son nom.
	 * 
	 * @param nom Le nom de l'entite.
	 * @return L'entite correspondante.
	 */
	public Entite get(String nom) throws ArrayIndexOutOfBoundsException {
		return this.tab[this.indice(nom)];
	}
	
	/**
	* <p> Insère une entité à l'indice i
	* </p>
	* @param i l'indice où insérer l'entité
	* @param o l'entité à insérer
 	*/
	public void insert (int i, Entite o) {
		Entite[] temp;

		temp = new Entite[this.tab.length + 1];
		copie(this.tab, temp, 0, 0, i);
		copie(this.tab, temp, i, i + 1, this.tab.length - i);
		temp[i] = o;

		this.tab = temp;
	}
	
	/**
	* <p> Affecte la valeur du tableau d'indice i
	* </p>
	* @param i l'indice du tableau à affecter
 	*/
	public void set (int i, Entite o) {
		this.tab[i] = o;
	}
	
	/**
	* <p> Donne la longueur du tableau
	* </p>
	* @return int correspondant à la longueur du tableau
 	*/
	public int taille() {
		return this.tab.length;
	}
	
	/**
	* <p> Renvoit selon si l'entité est dans le tableau
	* </p>
	* @param o l'entité à tester
	* @return booléen selon si o est dans le tableau
 	*/
	public boolean contient (Entite o) {
		return (this.indice(o) != -1);
	}
	
	/**
	* <p> Renvoit selon si une entité de même nom est dans le tableau
	* </p>
	* @param nom nom de l'entité à tester
	* @return booléen selon si une entité de même nom est dans le tableau
 	*/
	public boolean contient (String nom) {
		return (this.indice(nom) != -1);
	}
	
	/**
	* <p> Retire l'entité d'indice i du tableau
	* </p>
	* @param i indice de l'entité à retirer
	* @return l'entité retirée
 	*/
	public Entite retirer (int i) throws ArrayIndexOutOfBoundsException {
		Entite[] temp;
		Entite res;
		res = this.tab[i];
		temp = new Entite[this.tab.length - 1];
		copie(this.tab, temp, 0, 0, i);
		copie(this.tab, temp, i + 1, i, this.tab.length - i - 1);
		this.tab = temp;
		return res;
	}
	
	/**
	* <p> Retire l'entité correspondante du tableau
	* </p>
	* @param o entité à retirer
	* @return l'entité retirée
 	*/
	public Entite retirer (Entite o) throws ArrayIndexOutOfBoundsException {
		return this.retirer(this.indice(o));
	}
	
	/**
	* <p> Retire la première entité de même nom du tableau
	* </p>
	* @param nom nom de l'entité à retirer
	* @return l'entité retirée
 	*/
	public Entite retirer (String nom) throws ArrayIndexOutOfBoundsException {
		return this.retirer(this.indice(nom));
	}
	
	/**
	* <p> Renvoit les objets du tableau dynamique
	* </p>
	* @return tableau contenant les objets du tableau dynamique
 	*/
	public Objet[] getTabObjets() {
		Objet[] temp;
		temp = new Objet[this.tab.length];
		int n = 0;

		for (int i = 0; i < this.tab.length; i++) {
			Entite elt = this.tab[i];
			if (elt instanceof Objet) {
				temp[n] = (Objet) elt;
				n++;
			}
		}

		Objet[] res;
		res = new Objet[n];
		copie(temp, res, 0, 0, n);
		return res;
	}
	
	/**
	* <p> Renvoit les vivants du tableau dynamique
	* </p>
	* @return tableau contenant les vivants du tableau dynamique
 	*/
	public Vivant[] getTabVivants() {
		Vivant[] temp;
		temp = new Vivant[this.tab.length];
		int n = 0;
		
		for (int i=0;i<this.tab.length;i++) {
			Entite elt = this.tab[i];
			if (elt instanceof Vivant) {
				temp[n] = (Vivant) elt;
				n++;
			}
		}
		
		Vivant[] res;
		res = new Vivant[n];
		copie(temp,res,0,0,n);
		return res;
	}
	
	/**
	* <p> Convertit le tableau dynamique en string
	* </p>
 	* @return string représentant le tableau dynamique
 	*/
	@Override
	/**
	 * Retourne une representation sous forme de chaine de caracteres du tableau.
	 * 
	 * @return Une chaine decrivant le tableau et son contenu.
	 */
	public String toString() {
		StringBuilder s = new StringBuilder();
		s.append("TableauDynamique:");

		Objet[] tabO;
		tabO = this.getTabObjets();
		if (tabO.length > 0) {
			s.append("\nObjets :\n[");
			for (int i = 0; i < tabO.length; i++) {
				s.append(tabO[i].toString());
				s.append(", ");
			}
			s.append("]");
		}
		
		Vivant[] tabV;
		tabV = this.getTabVivants();
		if (tabV.length>0) {
			s.append("\nVivants :\n[");
			for (int i=0;i<tabV.length;i++) {
				s.append(tabV[i].toString());
				s.append(", ");
			}
			s.append("]");
		}
		
		if (tabO.length == 0 && tabV.length == 0) {
			s.append("vide");
		}
		return s.toString();
	}
}
