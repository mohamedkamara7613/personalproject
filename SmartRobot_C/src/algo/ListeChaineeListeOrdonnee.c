#include <stdlib.h>
#include <errno.h>
#include "ListeChaineeListeOrdonnee.h"

LCLO_ListeOrdonnee LCLO_listeOrdonnee(CLC_FonctionCopier copierElement,
                                      CLC_FonctionLiberer supprimerElement,
                                      CLC_FonctionComparer comparerElement) {
  LCLO_ListeOrdonnee l;

  l.liste = LC_listeChainee();
  l.copierElement = copierElement;
  l.supprimerElement = supprimerElement;
  l.comparer = comparerElement;
  l.longueur = 0;
  return l;
}

bool LCLO_estVide(LCLO_ListeOrdonnee liste) {
  return liste.longueur == 0;
}

int LCLO_longueur(LCLO_ListeOrdonnee liste) {
  return liste.longueur;
}

void* LCLO_element(LCLO_ListeOrdonnee liste, unsigned int position) {
  LC_ListeChainee cur;
  unsigned int i;

  if (liste.longueur == 0) {
    errno = LCLO_LISTE_VIDE_ERREUR;
    return NULL;
  }

  if (position < 0 || position > (unsigned int)liste.longueur-1) {
    errno = LCLO_POSITION_TROP_GRANDE_ERREUR;
    return NULL;
  }

  cur = liste.liste;
  for (i = 0; i < position; i++) {
    cur = LC_obtenirListeSuivante(cur);
  }

  errno = 0;
  return liste.copierElement(LC_obtenirElement(cur));
}

void LCLO_inserer(LCLO_ListeOrdonnee* pliste, void* element) {
  void* teteElem;              
  LC_ListeChainee prev;        
  LC_ListeChainee cur;         
  void* curElem;               
  LC_ListeChainee nouveau;     

  if (pliste->longueur == 0) {
    LC_ajouter(&(pliste->liste), element, pliste->copierElement);
    pliste->longueur++;
    errno = 0;
    return;
  }

  teteElem = LC_obtenirElement(pliste->liste);
  if (pliste->comparer(element, teteElem) <= 0) {
    LC_ajouter(&(pliste->liste), element, pliste->copierElement);
    pliste->longueur++;
    errno = 0;
    return;
  }

  prev = pliste->liste;
  cur  = LC_obtenirListeSuivante(prev);

  while (!LC_estVide(cur)) {
    curElem = LC_obtenirElement(cur);
    if (pliste->comparer(element, curElem) <= 0) {
      break;
    }
    prev = cur;
    cur = LC_obtenirListeSuivante(cur);
  }

  nouveau = LC_listeChainee();
  LC_ajouter(&nouveau, element, pliste->copierElement);
  LC_fixerListeSuivante(&nouveau, cur);
  LC_fixerListeSuivante(&prev, nouveau);

  pliste->longueur++;
  errno = 0;
}

void LCLO_supprimer(LCLO_ListeOrdonnee* pliste, unsigned int position) {
  LC_ListeChainee prev;   
  unsigned int i;         
  LC_ListeChainee cible;  

  if (position < 0 || position > pliste->longueur-1) {
    errno = LCLO_POSITION_TROP_GRANDE_ERREUR;
    return;
  }

  if (position == 0) {
    LC_supprimerTete(&(pliste->liste), pliste->supprimerElement);
    pliste->longueur--;
    errno = 0;
    return;
  }

  prev = pliste->liste;
  for (i = 0; i < position - 1; i++) {
    prev = LC_obtenirListeSuivante(prev);
  }
  cible = LC_obtenirListeSuivante(prev);
  LC_supprimerTete(&cible, pliste->supprimerElement);
  LC_fixerListeSuivante(&prev, cible);

  pliste->longueur--;
  errno = 0;
}

void LCLO_vider(LCLO_ListeOrdonnee* pliste) {
  LC_supprimer(&(pliste->liste), pliste->supprimerElement);
  pliste->longueur = 0;
}
