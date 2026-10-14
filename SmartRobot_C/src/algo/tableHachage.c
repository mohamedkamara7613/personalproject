#include <stdlib.h>
#include <errno.h>
#include <stddef.h>
#include "tableHachage.h"

/* -------------------------------------------------------------------------- */
/*                 FONCTIONS / VARIABLES PRIVEES AU MODULE                    */
/* -------------------------------------------------------------------------- */

typedef struct {
  void* pcle;
  void* pvaleur;
} TH_CleValeur;


static unsigned char TH_hash(const void* pcle, size_t tailleCle) {
  const unsigned char* p;
  size_t i;
  unsigned int somme;

  p = (const unsigned char*)pcle;
  somme = 0U;
  for (i = 0U; i < tailleCle; ++i) {
    somme += (unsigned int)p[i];
  }
  return (unsigned char)somme;
}

/* Ces pointeurs sont utilisés temporairement par TH_copierCleValeurProfondeur et TH_libererCleValeurProfondeur().
   On les POSITIONNE juste avant d'appeler ces deux fonctions. (Hypothèse mono-thread / contexte pédagogique.) */
static CLC_FonctionCopier g_copierCle = NULL;
static CLC_FonctionCopier g_copierValeur = NULL;
static CLC_FonctionLiberer g_libererCle = NULL;
static CLC_FonctionLiberer g_libererValeur = NULL;


static void* TH_copierCleValeurProfondeur(void* pcleValeur) {
  TH_CleValeur* pSrc;
  TH_CleValeur* pDst;

  pSrc = (TH_CleValeur*)pcleValeur;
  pDst = (TH_CleValeur*)malloc(sizeof(TH_CleValeur));
  if (pDst == NULL) {
    return NULL;
  }
  pDst->pcle = g_copierCle(pSrc->pcle);
  pDst->pvaleur = g_copierValeur(pSrc->pvaleur);
  return (void*)pDst;
}

static void TH_libererCleValeurProfondeur(void* pcleValeur) {
  TH_CleValeur* p;
  p = (TH_CleValeur*)pcleValeur;
  if (p != NULL) {
    if (g_libererCle != NULL && p->pcle != NULL) {
      g_libererCle(p->pcle);
    }
    if (g_libererValeur != NULL && p->pvaleur != NULL) {
      g_libererValeur(p->pvaleur);
    }
    free(p);
  }
}

static LC_ListeChainee TH_rechercherCleDansListe(LC_ListeChainee l,
						 void* pcle,
						 CLC_FonctionComparer comparerCle) {
  TH_CleValeur* pclevaleur;
  LC_ListeChainee listeSuivante;;
  if (!LC_estVide(l)) {
    pclevaleur = (TH_CleValeur*)LC_obtenirElement(l);
    if (comparerCle(pcle, pclevaleur->pcle) == 0) {
      return l;
    } else {
      listeSuivante = LC_obtenirListeSuivante(l);
      return TH_rechercherCleDansListe(listeSuivante, pcle, comparerCle);
    }
  } else
    return l;
}

static void TH_supprimerCleValeurDeLaListe(LC_ListeChainee* pl,
					   void* pcle,
					   CLC_FonctionComparer comparerCle) {
  TH_CleValeur* pclevaleur;
  LC_ListeChainee listeSuivante;;
  if (!LC_estVide(*pl)) {
    pclevaleur = (TH_CleValeur*)LC_obtenirElement(*pl);
    if (comparerCle(pcle, pclevaleur->pcle) == 0) {
      LC_supprimerTete(pl, TH_libererCleValeurProfondeur);
    } else {
      listeSuivante = LC_obtenirListeSuivante(*pl);
      TH_supprimerCleValeurDeLaListe(&listeSuivante, pcle, comparerCle);
      LC_fixerListeSuivante(pl, listeSuivante);
    }
  } else
    errno = TH_CLE_ABSENTE_ERREUR;
}


/* -------------------------------------------------------------------------- */
/*                    FONCTIONS PUBLIQUES DU MODULE                           */
/* -------------------------------------------------------------------------- */

TH_TableHachage TH_tableHachage(CLC_FonctionCopier copierCle,
                                CLC_FonctionLiberer libererCle,
                                CLC_FonctionComparer comparerCle,
                                size_t tailleCle,
                                CLC_FonctionCopier copierValeur,
                                CLC_FonctionLiberer libererValeur) {
  TH_TableHachage tableHachage;
  unsigned int i;

  tableHachage.tailleCle = tailleCle;
  tableHachage.copierCle = copierCle;
  tableHachage.libererCle = libererCle;
  tableHachage.comparerCle = comparerCle;
  tableHachage.copierValeur = copierValeur;
  tableHachage.libererValeur = libererValeur;
  tableHachage.nbElements = 0U;

  for (i = 0U; i < (unsigned int)TH_TAILLE_TABLE; ++i) {
    tableHachage.table[i] = LC_listeChainee();
  }

  return tableHachage;
}

bool TH_estVide(TH_TableHachage tableHachage) {
  return (tableHachage.nbElements == 0U) ? true : false;
}

unsigned int TH_taille(TH_TableHachage tableHachage) {
  return tableHachage.nbElements;
}

bool TH_contient(TH_TableHachage tableHachage, void* pcle) {
  unsigned char idx;

  idx = TH_hash(pcle, tableHachage.tailleCle);
  return TH_rechercherCleDansListe(tableHachage.table[(unsigned int)idx], pcle, tableHachage.comparerCle) != NULL;
}

void TH_inserer(TH_TableHachage* ptableHachage, void* pcle, void* pvaleur) {
  unsigned char idx;
  LC_ListeChainee l;
  TH_CleValeur* pclevaleur;
  TH_CleValeur tmp;
  void* pNewVal;

  idx = TH_hash(pcle, ptableHachage->tailleCle);
  l = TH_rechercherCleDansListe(ptableHachage->table[(unsigned int)idx], pcle, ptableHachage->comparerCle);
  if (LC_estVide(l)) {
    g_copierCle = ptableHachage->copierCle;
    g_copierValeur = ptableHachage->copierValeur;
    tmp.pcle = pcle;
    tmp.pvaleur = pvaleur;
    LC_ajouter(&(ptableHachage->table[(unsigned int)idx]), (void*)&tmp, TH_copierCleValeurProfondeur);
    ptableHachage->nbElements += 1U;
  } else {
    pclevaleur = (TH_CleValeur*)LC_obtenirElement(l);
    pNewVal = ptableHachage->copierValeur(pvaleur);
    if (pNewVal == NULL) {
      errno = TH_MEMOIRE_ERREUR;
      return;
    }
    ptableHachage->libererValeur(pclevaleur->pvaleur);
    pclevaleur->pvaleur = pNewVal;
  }
  errno = 0;
}


void TH_supprimer(TH_TableHachage* ptableHachage, void* pcle) {
  unsigned char idx;

  idx = TH_hash(pcle, ptableHachage->tailleCle);
  g_libererCle = ptableHachage->libererCle;
  g_libererValeur = ptableHachage->libererValeur;
  errno = 0;
  TH_supprimerCleValeurDeLaListe(&(ptableHachage->table[(unsigned int)idx]), pcle, ptableHachage->comparerCle);
  if (errno == 0) {
      ptableHachage->nbElements -= 1U;
  }
}

void* TH_valeur(TH_TableHachage tableHachage, void* pcle) {
  unsigned char idx;
  LC_ListeChainee l;
  TH_CleValeur* pclevaleur;
  void* pCopie;

  idx = TH_hash(pcle, tableHachage.tailleCle);
  l = TH_rechercherCleDansListe(tableHachage.table[(unsigned int)idx], pcle, tableHachage.comparerCle);
  if (!LC_estVide(l)) {
    pclevaleur = (TH_CleValeur*)LC_obtenirElement(l);
    pCopie = tableHachage.copierValeur(pclevaleur->pvaleur);
    if (pCopie == NULL) {
      errno = TH_MEMOIRE_ERREUR;
      return NULL;
    }
    errno = 0;
    return pCopie;
  };
  errno = TH_CLE_ABSENTE_ERREUR;
  return NULL;
}

void** TH_cles(TH_TableHachage tableHachage) {
  void** pTab = (void**)malloc(tableHachage.nbElements * sizeof(void*));
  unsigned int i;
  unsigned int j;
  TH_CleValeur* pclevaleur;
  if (pTab == NULL) {
    errno = TH_MEMOIRE_ERREUR;
    return NULL;
  }
  j = 0U;
  for (i = 0U; i < (unsigned int)TH_TAILLE_TABLE; ++i) {
    LC_ListeChainee l = tableHachage.table[i];
    while (!LC_estVide(l)) {
      pclevaleur = (TH_CleValeur*)LC_obtenirElement(l);
      pTab[j] = tableHachage.copierCle(pclevaleur->pcle);
      if (pTab[j] == NULL) {
	unsigned int k;
	for (k = 0U; k < j; ++k) {
	  tableHachage.libererCle(pTab[k]);
	}
	free(pTab);
	errno = TH_MEMOIRE_ERREUR;
	return NULL;
      }
      j += 1U;
      l = LC_obtenirListeSuivante(l);
    }
  }
  errno = 0;
  return pTab;
}


void TH_vider(TH_TableHachage* ptableHachage) {
  unsigned int i;

  for (i = 0U; i < (unsigned int)TH_TAILLE_TABLE; ++i) {
    while (!LC_estVide(ptableHachage->table[i])) {
      g_libererCle = ptableHachage->libererCle;
      g_libererValeur = ptableHachage->libererValeur;
      LC_supprimerTete(&(ptableHachage->table[i]), TH_libererCleValeurProfondeur);
      if (ptableHachage->nbElements > 0U) {
        ptableHachage->nbElements -= 1U;
      }
    }
  }
  errno = 0;
}
