#include <math.h>
#include <stdlib.h>
#include <string.h>
#include "copieLiberationComparaisonTypesSimples.h"

void* CLCTS_copierGenerique(void* p, size_t taille) {
    void* copie = malloc(taille);
    if (copie == NULL) {
	return NULL; // Gestion de l'erreur d'allocation mémoire
    }
    memcpy(copie, p, taille);
    return copie;
}

void CLCTS_libererGenerique(void* p) {
    free(p);
}

void* CLCTS_copierChar(void* p) {
    return CLCTS_copierGenerique(p, sizeof(char));
}

void CLCTS_libererChar(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerChar(void* p1, void* p2) {
    char c1 = *(char*)p1;
    char c2 = *(char*)p2;
    if (c1 < c2) return -1;
    if (c1 > c2) return 1;
    return 0;
}

int CLCTS_comparerUnsignedChar(void* p1, void* p2) {
    unsigned char c1 = *(unsigned char*)p1;
    unsigned char c2 = *(unsigned char*)p2;
    if (c1 < c2) return -1;
    if (c1 > c2) return 1;
    return 0;
}

void* CLCTS_copierInt(void* p) {
    return CLCTS_copierGenerique(p, sizeof(int));
}

void CLCTS_libererInt(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerInt(void* p1, void* p2) {
    int i1 = *(int*)p1;
    int i2 = *(int*)p2;
    if (i1 < i2) return -1;
    if (i1 > i2) return 1;
    return 0;
}

int CLCTS_comparerUnsignedInt(void* p1, void* p2) {
    unsigned int i1 = *(unsigned int*)p1;
    unsigned int i2 = *(unsigned int*)p2;
    if (i1 < i2) return -1;
    if (i1 > i2) return 1;
    return 0;
}

void* CLCTS_copierLong(void* p) {
    return CLCTS_copierGenerique(p, sizeof(long));
}

void CLCTS_libererLong(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerLong(void* p1, void* p2) {
    long l1 = *(long*)p1;
    long l2 = *(long*)p2;
    if (l1 < l2) return -1;
    if (l1 > l2) return 1;
    return 0;
}

int CLCTS_comparerUnsignedLong(void* p1, void* p2) {
    unsigned long l1 = *(unsigned long*)p1;
    unsigned long l2 = *(unsigned long*)p2;
    if (l1 < l2) return -1;
    if (l1 > l2) return 1;
    return 0;
}

void* CLCTS_copierLongLong(void* p) {
    return CLCTS_copierGenerique(p, sizeof(long long));
}

void CLCTS_libererLongLong(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerLongLong(void* p1, void* p2) {
    long long ll1 = *(long long*)p1;
    long long ll2 = *(long long*)p2;
    if (ll1 < ll2) return -1;
    if (ll1 > ll2) return 1;
    return 0;
}

int CLCTS_comparerUnsignedLongLong(void* p1, void* p2) {
    unsigned long long ll1 = *(unsigned long long*)p1;
    unsigned long long ll2 = *(unsigned long long*)p2;
    if (ll1 < ll2) return -1;
    if (ll1 > ll2) return 1;
    return 0;
}

void* CLCTS_copierFloat(void* p) {
    return CLCTS_copierGenerique(p, sizeof(float));
}

void CLCTS_libererFloat(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerFloat(void* p1, void* p2) {
    float f1 = *(float*)p1;
    float f2 = *(float*)p2;
    if (fabs(f1 - f2) < CLCTS_EPSILON_COMPARAISON_FLOAT) return 0;
    if (f1 < f2) return -1;
    return 1;
}

void* CLCTS_copierDouble(void* p) {
    return CLCTS_copierGenerique(p, sizeof(double));
}

void CLCTS_libererDouble(void* p) {
    CLCTS_libererGenerique(p);
}

int CLCTS_comparerDouble(void* p1, void* p2) {
    double d1 = *(double*)p1;
    double d2 = *(double*)p2;
    if (fabs(d1 - d2) < CLCTS_EPSILON_COMPARAISON_DOUBLE) return 0;
    if (d1 < d2) return -1;
    return 1;
}

