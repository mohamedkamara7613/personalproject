/**
 * \file copieLiberationComparaisonTypesSimples.h
 * \brief Fonctions de copie, liberation et comparaison pour les types simples du C
 * \author Nicolas Delestre
 * \version 0.1
 * \date 2025
 **/
#ifndef __COPIELIBERATIONCOMPARAISONTYPESIMPLE_H__
#define __COPIELIBERATIONCOMPARAISONTYPESIMPLE_H__


/**
 * \def CLCTS_EPSILON_COMPARAISON_FLOAT
 * \brief Epsilon pour la comparaison de float
 **/
#define CLCTS_EPSILON_COMPARAISON_FLOAT 0.00001
/**
 * \def CLCTS_EPSILON_COMPARAISON_DOUBLE
 * \brief Epsilon pour la comparaison de double
 **/
#define CLCTS_EPSILON_COMPARAISON_DOUBLE 0.0000001

/**
 * \fn CLCTS_copierChar
 * \brief Fonction de copie pour le type char
 * \param void* Pointeur vers la donnée à copier (doit être un char)
 * \return void* Pointeur vers la copie de la donnée (doit être un char)
 **/
void* CLCTS_copierChar(void*);
/**
 * \fn CLCTS_libererChar
 * \brief Fonction de libération pour le type char
 * \param void* Pointeur vers la donnée à libérer (doit être un char)
 **/
void CLCTS_libererChar(void*);
/**
 * \fn CLCTS_comparerChar
 * \brief Fonction de comparaison pour le type char
 * \param void* Pointeur vers la première donnée à comparer (doit être un char)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un char)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerChar(void*, void*);
/**
 * \fn CLCTS_comparerUnsignedChar
 * \brief Fonction de comparaison pour le type unsigned char
 * \param void* Pointeur vers la première donnée à comparer (doit être un unsigned char)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un unsigned char)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerUnsignedChar(void*, void*);

/**
 * \fn CLCTS_copierInt
 * \brief Fonction de copie pour le type int
 * \param void* Pointeur vers la donnée à copier (doit être un int)
 * \return void* Pointeur vers la copie de la donnée (doit être un int)
 **/
void* CLCTS_copierInt(void*);
/**
 * \fn CLCTS_libererInt
 * \brief Fonction de libération pour le type int
 * \param void* Pointeur vers la donnée à libérer (doit être un int)
 **/
void CLCTS_libererInt(void*);
/**
 * \fn CLCTS_comparerInt
 * \brief Fonction de comparaison pour le type int
 * \param void* Pointeur vers la première donnée à comparer (doit être un int)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un int)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerInt(void*, void*);
/**
 * \fn CLCTS_comparerUnsignedInt
 * \brief Fonction de comparaison pour le type unsigned int
 * \param void* Pointeur vers la première donnée à comparer (doit être un unsigned int)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un unsigned int)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerUnsignedInt(void*, void*);

/**
 * \fn CLCTS_copierShort
 * \brief Fonction de copie pour le type short
 * \param void* Pointeur vers la donnée à copier (doit être un short)
 * \return void* Pointeur vers la copie de la donnée (doit être un short)
 **/
void* CLCTS_copierLong(void*);
/**
 * \fn CLCTS_libererShort
 * \brief Fonction de libération pour le type short
 * \param void* Pointeur vers la donnée à libérer (doit être un short)
 **/
void CLCTS_libererLong(void*);
/**
 * \fn CLCTS_comparerShort
 * \brief Fonction de comparaison pour le type short
 * \param void* Pointeur vers la première donnée à comparer (doit être un short)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un short)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerLong(void*, void*);
/**
 * \fn CLCTS_comparerUnsignedShort
 * \brief Fonction de comparaison pour le type unsigned short
 * \param void* Pointeur vers la première donnée à comparer (doit être un unsigned short)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un unsigned short)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerUnsignedLong(void*, void*);

/**
 * \fn CLCTS_copierLongLong
 * \brief Fonction de copie pour le type long long
 * \param void* Pointeur vers la donnée à copier (doit être un long long)
 * \return void* Pointeur vers la copie de la donnée (doit être un long long)
 **/
void* CLCTS_copierLongLong(void*);
/**
 * \fn CLCTS_libererLongLong
 * \brief Fonction de libération pour le type long long
 * \param void* Pointeur vers la donnée à libérer (doit être un long long)
 **/
void CLCTS_libererLongLong(void*);
/**
 * \fn CLCTS_comparerLongLong
 * \brief Fonction de comparaison pour le type long long
 * \param void* Pointeur vers la première donnée à comparer (doit être un long long)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un long long)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerLongLong(void*, void*);
/**
 * \fn CLCTS_comparerUnsignedLongLong
 * \brief Fonction de comparaison pour le type unsigned long long
 * \param void* Pointeur vers la première donnée à comparer (doit être un unsigned long long)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un unsigned long long)
 * \return int 0 si les deux données sont égales, -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerUnsignedLongLong(void*, void*);

/**
 * \fn CLCTS_copierFloat
 * \brief Fonction de copie pour le type float
 * \param void* Pointeur vers la donnée à copier (doit être un float)
 * \return void* Pointeur vers la copie de la donnée (doit être un float)
 **/
void* CLCTS_copierFloat(void*);
/**
 * \fn CLCTS_libererFloat
 * \brief Fonction de libération pour le type float
 * \param void* Pointeur vers la donnée à libérer (doit être un float)
 **/
void CLCTS_libererFloat(void*);
/**
 * \fn CLCTS_comparerFloat
 * \brief Fonction de comparaison pour le type float
 * \param void* Pointeur vers la première donnée à comparer (doit être un float)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un float)
 * \return int 0 si les deux données sont égales (avec une marge d'erreur définie par CLCTS_EPSILON_COMPARAISON_FLOAT), -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerFloat(void*, void*);

/**
 * \fn CLCTS_copierDouble
 * \brief Fonction de copie pour le type double
 * \param void* Pointeur vers la donnée à copier (doit être un double)
 * \return void* Pointeur vers la copie de la donnée (doit être un double)
 **/
void* CLCTS_copierDouble(void*);
/**
 * \fn CLCTS_libererDouble
 * \brief Fonction de libération pour le type double
 * \param void* Pointeur vers la donnée à libérer (doit être un double)
 **/
void CLCTS_libererDouble(void*);
/**
 * \fn CLCTS_comparerDouble
 * \brief Fonction de comparaison pour le type double
 * \param void* Pointeur vers la première donnée à comparer (doit être un double)
 * \param void* Pointeur vers la deuxième donnée à comparer (doit être un double)
 * \return int 0 si les deux données sont égales (avec une marge d'erreur définie par CLCTS_EPSILON_COMPARAISON_DOUBLE), -1 si la première est inférieure à la deuxième, 1 sinon
 **/
int CLCTS_comparerDouble(void*, void*);


#endif // __COPIELIBERATIONCOMPARAISONTYPESIMPLE_H__
