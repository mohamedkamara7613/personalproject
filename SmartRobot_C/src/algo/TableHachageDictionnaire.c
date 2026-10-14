#include <stdlib.h>
#include <errno.h>
#include <stddef.h>
#include "TableHachageDictionnaire.h"

THD_Dictionnaire THD_dictionnaire(CLC_FonctionCopier copierCle,
                                CLC_FonctionLiberer libererCle,
                                CLC_FonctionComparer comparerCle,
                                size_t tailleCle,
                                CLC_FonctionCopier copierValeur,
                                CLC_FonctionLiberer libererValeur) {
  return TH_tableHachage(copierCle,
			 libererCle,
			 comparerCle,
			 tailleCle,
			 copierValeur,
			 libererValeur);
}

bool THD_estVide(THD_Dictionnaire dico) {
  return TH_estVide(dico);
}

unsigned int THD_taille(THD_Dictionnaire dico) {
  return TH_taille(dico);
}

bool THD_contient(THD_Dictionnaire dico, void* pcle) {
  return TH_contient(dico, pcle);
}

void THD_inserer(THD_Dictionnaire* pdico, void* pcle, void* pvaleur) {
  TH_inserer(pdico, pcle, pvaleur);
}


void THD_supprimer(THD_Dictionnaire* pdico, void* pcle) {
  TH_supprimer(pdico, pcle);
}

void* THD_valeur(THD_Dictionnaire dico, void* pcle) {
  return TH_valeur(dico, pcle);
}

LCL_Liste THD_cles(THD_Dictionnaire dico) {
  void** tableCles = TH_cles(dico);
  LCL_Liste res = LCL_liste(dico.copierCle,
			    dico.libererCle);
  unsigned int i;
  if (tableCles != NULL) {
    for (i = 0U; i < dico.nbElements; ++i) {
      LCL_inserer(&res, tableCles[i], 0);
      dico.libererCle(tableCles[i]);
    }
    free(tableCles);
  }
  return res;
}


void THD_vider(THD_Dictionnaire* pdico) {
  TH_vider(pdico);
}
