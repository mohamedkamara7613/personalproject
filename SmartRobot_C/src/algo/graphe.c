#include "graphe.h"
#include "copieLiberationComparaisonTypesSimples.h"

void* G_copierArc(void* parc) {
  if (parc == NULL) {
    errno = G_SOMMET_ERREUR;
    return NULL;
  }
  G_Arc* copie = malloc(sizeof(G_Arc));
  if (copie == NULL) {
    errno = G_MEMOIRE_ERREUR;
    return NULL;
  }
  errno = 0;
  copie->src = ((G_Arc*)parc)->src;
  copie->dest = ((G_Arc*)parc)->dest;
  return copie;
}

void G_libererArc(void* parc) {
  if (parc != NULL) {
    free(parc);
  }
}

int G_comparerArcs(void* parc1, void* parc2) {
  if (parc1 == NULL || parc2 == NULL) {
    errno = G_SOMMET_ERREUR;
    return 1;
  }
  errno = 0;
  G_Arc arc1 = *((G_Arc*)parc1);
  G_Arc arc2 = *((G_Arc*)parc2);
  return (arc1.src == arc2.src && arc1.dest == arc2.dest) ? 0 : 1;
}

G_Graphe G_graphe(bool oriente,
		  void* (*copierEtiquette) (void*),
		  void (*libererEtiquette) (void*),
		  int (*comparerEtiquettes) (void*, void*),
		  void* (*copierValeur) (void*),
		  void (*libererValeur) (void*),
		  int (*comparerValeurs) (void*, void*)) {
  G_Graphe g;
  g.oriente = oriente;
  g.sommets = LCL_liste(CLCTS_copierInt, CLCTS_libererInt);
  g.arcs = LCL_liste(G_copierArc, G_libererArc);
  g.etiquettes = THD_dictionnaire(CLCTS_copierInt, CLCTS_libererInt, CLCTS_comparerInt,
				  sizeof(int),
				  copierEtiquette, libererEtiquette);
  g.copierEtiquette = copierEtiquette;
  g.libererEtiquette = libererEtiquette;
  g.comparerEtiquettes = comparerEtiquettes;
  g.valeurs = THD_dictionnaire(G_copierArc, G_libererArc, G_comparerArcs,
			      sizeof(G_Arc),
			      copierValeur, libererValeur);
  g.copierValeur = copierValeur;
  g.libererValeur = libererValeur;
  g.comparerValeurs = comparerValeurs;

  errno = 0;
  if ((copierEtiquette == NULL || libererEtiquette == NULL || comparerEtiquettes == NULL) &&
      (copierEtiquette != NULL || libererEtiquette != NULL || comparerEtiquettes != NULL)) {
    errno = G_GRAPHE_INCOHERENT_ERREUR;
  }
  if ((copierValeur == NULL || libererValeur == NULL || comparerValeurs == NULL) &&
      (copierValeur != NULL || libererValeur != NULL || comparerValeurs != NULL)) {
    errno = G_GRAPHE_INCOHERENT_ERREUR;
  }
  return g;
}

int G_ajouterSommet(G_Graphe *pg, unsigned int id, void *petiquette) {
  if (petiquette != NULL && pg->copierEtiquette == NULL) {
    errno = G_GRAPHE_NON_ETIQUETE_ERREUR;
    return -1;
  }
  if (G_sommetPresent(*pg, id)) {
    errno = G_SOMMET_ERREUR;
    return -1;
  }
  errno = 0;
  LCL_inserer(&pg->sommets, &id, LCL_longueur(pg->sommets));
  if (petiquette != NULL) {
    THD_inserer(&pg->etiquettes, &id, petiquette);
  }
  return id;
}

int G_ajouterArc(G_Graphe *pg, unsigned int idSrc, unsigned int idDest, void *pvaleur) {
  if (pvaleur != NULL && pg->copierValeur == NULL) {
    errno = G_GRAPHE_NON_VALUE_ERREUR;
    return -1;
  }
  G_Arc arc;
  arc.src = idSrc;
  arc.dest = idDest;
  LCL_inserer(&pg->arcs, &arc, LCL_longueur(pg->arcs));
  if (pvaleur != NULL) {
    THD_inserer(&pg->valeurs, &arc, pvaleur);
  }
  return 0;
}

bool G_sommetPresent(G_Graphe g, unsigned int id) {
  int sommetCourant;
  int *temp;
  for (int i = 0; i <= LCL_longueur(g.sommets)-1; ++i) {
    temp = (int*)LCL_element(g.sommets, i);
    sommetCourant = *temp;
    free(temp);
    if (sommetCourant == (int)id) {
      return true;
    }
  }
  return false;
}

bool G_arcPresent(G_Graphe g, unsigned int idSrc, unsigned int idDest) {
  G_Arc arcCourant;
  G_Arc *temp;
  for (int i = 0; i <= LCL_longueur(g.arcs)-1; ++i) {
    temp = (G_Arc*)LCL_element(g.arcs, i);
    arcCourant = *temp;
    free(temp);
    if (arcCourant.src == (int)idSrc && arcCourant.dest == (int)idDest) {
      return true;
    }
    if (!g.oriente && arcCourant.src == (int)idDest && arcCourant.dest == (int)idSrc) {
	return true;
    }
  }
  return false;
}

static void G_supprimerArcsDUnSommet(G_Graphe *pg, unsigned int id) {
  for(int i=0; i<=LCL_longueur(pg->arcs)-1; i++) {
    G_Arc *temp = (G_Arc*)LCL_element(pg->arcs, i);
    if(temp->src == (int)id || temp->dest == (int)id) {
      LCL_supprimer(&pg->arcs, i);
      free(temp);
      i--;
    } else {
      free(temp);
    }
  }
}

static void G_supprimerEtiquetteDUnSommet(G_Graphe *pg, unsigned int id) {
  THD_supprimer(&pg->etiquettes, &id);
}

int G_supprimerSommet(G_Graphe *pg, unsigned int id) {
  bool trouve = false;
  for(int i=0; i<=LCL_longueur(pg->sommets)-1; i++) {
    int *temp = (int*)LCL_element(pg->sommets, i);
    if(*temp == (int)id) {
      LCL_supprimer(&pg->sommets, i);
      free(temp);
      trouve = true;
      break;
    }
    free(temp);
  }
  if(!trouve) {
    errno = G_SOMMET_ERREUR;
    return -1;
  } 
  G_supprimerArcsDUnSommet(pg, id);
  if (pg->copierEtiquette != NULL)
    G_supprimerEtiquetteDUnSommet(pg, id);
  return 0;
}

int G_supprimerArc(G_Graphe *pg, unsigned int idSrc, unsigned int idDest) {
  int res = -1;
  for(int i=0; i<=LCL_longueur(pg->arcs)-1; i++) {
    G_Arc *temp = (G_Arc*)LCL_element(pg->arcs, i);
    if(temp->src == (int)idSrc && temp->dest == (int)idDest) {
      LCL_supprimer(&pg->arcs, i);
      res = 0;
    }
    if(!pg->oriente && temp->src == (int)idDest && temp->dest == (int)idSrc) {
      LCL_supprimer(&pg->arcs, i);
      res = 0;
    }
    free(temp);
  }
  if (res == 0 && pg->copierValeur != NULL) {
    G_Arc arc;
    arc.src = idSrc;
    arc.dest = idDest;
    THD_supprimer(&pg->valeurs, &arc);
    if (!pg->oriente) {
      G_Arc arcInverse;
      arcInverse.src = idDest;
      arcInverse.dest = idSrc;
      THD_supprimer(&pg->valeurs, &arcInverse);
    }
  }
  return res;
}

LCL_Liste G_sommets(G_Graphe g) {
  return LCL_copier(g.sommets);
}

LCL_Liste G_obtenirSommetsAdjacents(G_Graphe g, unsigned int idSrc) {
  LCL_Liste res = LCL_liste(CLCTS_copierInt, CLCTS_libererInt);
  for(int i=0; i<=LCL_longueur(g.arcs)-1; i++) {
    G_Arc *temp = (G_Arc*)LCL_element(g.arcs, i);
    if(temp->src == (int)idSrc) {
      LCL_inserer(&res, &temp->dest, LCL_longueur(res));
    }
    if(!g.oriente && temp->dest == (int)idSrc) {
      LCL_inserer(&res, &temp->src, LCL_longueur(res));
    }
    free(temp);
  }
  return res;
}

void* G_obtenirEtiquette(G_Graphe g, unsigned int id) {
  if (g.copierEtiquette == NULL) {
    errno = G_GRAPHE_NON_ETIQUETE_ERREUR;
    return NULL;
  }
  void *petiquette = NULL;
  if (THD_contient(g.etiquettes, &id)) {
    petiquette = THD_valeur(g.etiquettes, &id);
  } else {
    errno = G_SOMMET_ERREUR;
  }
  return petiquette;
}

int G_fixerEtiquette(G_Graphe *pg, unsigned int id, void *petiquette) {
  if (pg->copierEtiquette == NULL) {
    errno = G_GRAPHE_NON_ETIQUETE_ERREUR;
    return -1;
  }
  THD_inserer(&pg->etiquettes, &id, petiquette);
  return 0;
}

void* G_obtenirValeur(G_Graphe g, unsigned int idSrc, unsigned int idDest) {
  if (g.copierValeur == NULL) {
    errno = G_GRAPHE_NON_VALUE_ERREUR;
    return NULL;
  }
  G_Arc arc, arcInverse;
  arc.src = idSrc;
  arc.dest = idDest;
  arcInverse.src = idDest;
  arcInverse.dest = idSrc;
  void *pvaleur = NULL;
  if (THD_contient(g.valeurs, &arc)) {
    pvaleur = THD_valeur(g.valeurs, &arc);
  } else if (!g.oriente && THD_contient(g.valeurs, &arcInverse)) {
    pvaleur = THD_valeur(g.valeurs, &arcInverse);
  } else {
    errno = G_ARC_ERREUR;
  }
  return pvaleur;
}

int G_fixerValeur(G_Graphe *pg, unsigned int idSrc, unsigned int idDest, void *pvaleur) {
  if (pg->copierValeur == NULL) {
    errno = G_GRAPHE_NON_VALUE_ERREUR;
    return -1;
  }
  G_Arc arc, arcInverse;
  arc.src = idSrc;
  arc.dest = idDest;
  arcInverse.src = idDest;
  arcInverse.dest = idSrc;
  if (!THD_contient(pg->valeurs, &arc)) {
    if (!pg->oriente && THD_contient(pg->valeurs, &arcInverse) == false) {
      errno = G_ARC_ERREUR;
      return -1;
    }
    if (!pg->oriente) {
      THD_inserer(&pg->valeurs, &arcInverse, pvaleur);
      return 0;
    }
  }
  THD_inserer(&pg->valeurs, &arc, pvaleur);
  return 0;
}

void G_vider(G_Graphe *pg) {
  LCL_vider(&pg->sommets);
  LCL_vider(&pg->arcs);
  THD_vider(&pg->etiquettes);
  THD_vider(&pg->valeurs);
}



