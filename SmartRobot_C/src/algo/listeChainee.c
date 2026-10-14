#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <stdbool.h>
#include "listeChainee.h"

LC_ListeChainee LC_listeChainee(){
  errno=0;
  return NULL;
}

int LC_estVide(LC_ListeChainee l) {
  errno=0;
  return (l==NULL);
}

void LC_ajouter(LC_ListeChainee* pl, void* source, CLC_FonctionCopier copierElement) {
  LC_ListeChainee pNoeud=(LC_ListeChainee)malloc(sizeof(LC_Noeud));
  void* donnee=copierElement(source);
  if ((pNoeud!=NULL) && (donnee!=NULL)) {
      errno=0;
      pNoeud->lElement=donnee;
      pNoeud->listeSuivante=*pl;
      *pl=pNoeud;
  } else {
    errno=LC_ERREUR_MEMOIRE;
  }
}

void*  LC_obtenirElement(LC_ListeChainee l) {
  assert(!LC_estVide(l));
  errno=0;
  return l->lElement;
}

LC_ListeChainee LC_obtenirListeSuivante(LC_ListeChainee l) {
  assert(!LC_estVide(l));
  errno=0;
  return l->listeSuivante;
}

void LC_fixerElement(LC_ListeChainee* pl, void* element,CLC_FonctionCopier copierElement,CLC_FonctionLiberer libereElement) {
  void* donnee;

  assert(!LC_estVide(*pl));
  errno=0;
  libereElement(LC_obtenirElement(*pl));
  donnee=copierElement(element);
  if (donnee!=NULL) {
    (*pl)->lElement=donnee;
  }  else {
    errno=LC_ERREUR_MEMOIRE;
  } 
}

void LC_fixerListeSuivante(LC_ListeChainee* pl, LC_ListeChainee suivant) {
  assert(!LC_estVide(*pl));
  errno=0;
  (*pl)->listeSuivante=suivant;
}

void LC_supprimerTete(LC_ListeChainee* pl, CLC_FonctionLiberer libererElement){
  LC_ListeChainee temp;
  assert(!LC_estVide(*pl));
  errno=0;
  temp=*pl;
  *pl=LC_obtenirListeSuivante(*pl);
  libererElement(LC_obtenirElement(temp));
  free(temp);
}

void LC_supprimer(LC_ListeChainee* pl, CLC_FonctionLiberer libererElement){

  errno=0;
  if (!LC_estVide(*pl)) {
    LC_supprimerTete(pl,libererElement);
    LC_supprimer(pl,libererElement);
  } 
}

LC_ListeChainee LC_copier(LC_ListeChainee l,CLC_FonctionCopier copierElement) {
  LC_ListeChainee temp;

  errno=0;
  if (LC_estVide(l))
    return LC_listeChainee();
  else {
    temp=LC_copier(LC_obtenirListeSuivante(l),copierElement);
    LC_ajouter(&temp,LC_obtenirElement(l),copierElement);
    return temp;
  }
}

int LC_egales(LC_ListeChainee l1,LC_ListeChainee l2,CLC_FonctionComparer elementsEgaux) {
  errno=0;
  if (LC_estVide(l1) && LC_estVide(l2))
    return true;
  else {
    if (LC_estVide(l1) || LC_estVide(l2))
      return false;
    else {
      if (elementsEgaux(LC_obtenirElement(l1),LC_obtenirElement(l2)))
	return LC_egales(LC_obtenirListeSuivante(l1),LC_obtenirListeSuivante(l2),elementsEgaux);
      else
	return false;
    }
  }
}


