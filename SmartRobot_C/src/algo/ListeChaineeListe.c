#include <stdlib.h>
#include <errno.h>
#include "ListeChaineeListe.h"

LCL_Liste LCL_liste(CLC_FonctionCopier copierElement,
                    CLC_FonctionLiberer supprimerElement) {
  LCL_Liste l;
  l.liste = LC_listeChainee();
  l.copierElement = copierElement;
  l.supprimerElement = supprimerElement;
  l.longueur = 0;
  return l;
}

bool LCL_estVide(LCL_Liste liste) {
  return LC_estVide(liste.liste);
}

int LCL_longueur(LCL_Liste liste) {
  return liste.longueur;
}

void LCL_inserer(LCL_Liste* pliste, void* element, unsigned int position) {
  LC_ListeChainee cur;           
  LC_ListeChainee suiv;          
  unsigned int i;
  if (pliste == NULL) {
    errno = EINVAL;
    return;
  }
  if (position < 0 || position > (unsigned int)(pliste->longueur)) {
    errno = POSITION_HORS_BORNES_ERREUR;
    return;
  }
  if (position == 0) {
    LC_ajouter(&(pliste->liste), element, pliste->copierElement);
  } else {
    cur = pliste->liste;
    for (i = 0; i < position-1; i++) {
      cur = LC_obtenirListeSuivante(cur);
    }
    suiv = LC_obtenirListeSuivante(cur);
    LC_ajouter(&suiv, element, pliste->copierElement);
    LC_fixerListeSuivante(&cur, suiv);
  }

  pliste->longueur++;
  errno = 0;
}

void LCL_supprimer(LCL_Liste* pliste, unsigned int position) {
  LC_ListeChainee cur;   
  LC_ListeChainee suiv;  
  unsigned int i;

  if (pliste == NULL) {
    errno = EINVAL;
    return;
  }

  if (pliste->longueur == 0) {
    errno = LISTE_VIDE_ERREUR;
    return;
  }
  if (position < 0 || position >= (unsigned int)pliste->longueur) {
    errno = POSITION_HORS_BORNES_ERREUR;
    return;
  }
  if (position == 0) {
    LC_supprimerTete(&(pliste->liste), pliste->supprimerElement);
  } else {
    cur = pliste->liste;
    for (i = 0; i < position - 1; i++) {
      cur = LC_obtenirListeSuivante(cur);
    }
    suiv = LC_obtenirListeSuivante(cur);
    LC_supprimerTete(&suiv, pliste->supprimerElement);
    LC_fixerListeSuivante(&cur, suiv);
  }
  pliste->longueur--;
  errno = 0;
}

void* LCL_element(LCL_Liste liste, unsigned int position) {
  LC_ListeChainee cur;
  unsigned int i;

  if (liste.longueur == 0) {
    errno = LISTE_VIDE_ERREUR;
    return NULL;
  }
  if (position < 0 || position > (unsigned int)liste.longueur) {
    errno = POSITION_HORS_BORNES_ERREUR;
    return NULL;
  }
  cur = liste.liste;
  for (i = 0; i < position; i++) {
    cur = LC_obtenirListeSuivante(cur);
  }
  errno = 0;
  return liste.copierElement(LC_obtenirElement(cur));
}

LCL_Liste LCL_copier(LCL_Liste liste) {
  LCL_Liste nouvelleListe;
  nouvelleListe.liste = LC_copier(liste.liste, liste.copierElement);
  nouvelleListe.copierElement = liste.copierElement;
  nouvelleListe.supprimerElement = liste.supprimerElement;
  nouvelleListe.longueur = liste.longueur;
  return nouvelleListe;
}

void LCL_vider(LCL_Liste* pliste) {
  errno = 0;
  LC_supprimer(&(pliste->liste), pliste->supprimerElement);
  pliste->longueur = 0;
}
