def sac(masses, prix, masseMax):
    """
    Résout le problème du sac à dos en utilisant une approche de programmation dynamique.

    Parameters
    ----------
    masses : list of int
        Liste des masses des objets.
    prix : list of int
        Liste des prix des objets.
    masseMax : float
        Masse maximale que le sac peut contenir.

    Returns
    -------
    list of int
        Liste contenant des 0 et des 1 indiquant quels objets sont choisis.
    """
    # Dictionnaire pour mémoriser les solutions déjà calculées
    dejaVu = {}

    # Fonction pour calculer le prix d'un sac donné
    def prixChoix(choix):
        return sum(choix[i] * prix[i] for i in range(len(choix)))

    # Fonction de recherche pour déterminer les choix optimaux
    def recherche(k, mMax):
        # Si la clé (k, mMax) n'a pas encore été calculée
        if (k, mMax) not in dejaVu:
            # Cas de base : un seul objet à considérer
            if k == 1:
                if masses[0] <= mMax:
                    dejaVu[(1, mMax)] = [1]
                else:
                    dejaVu[(1, mMax)] = [0]
            else:
                # Si la masse du k-ème objet est supérieure à mMax
                if masses[k - 1] > mMax:
                    recherche(k - 1, mMax)
                    choixOptimal = dejaVu[(k - 1, mMax)] + [0]
                else:
                    # Sinon, on considère deux cas :
                    # 1. Ne pas prendre l'objet k-1
                    recherche(k - 1, mMax)
                    choixSansObjet = dejaVu[(k - 1, mMax)]

                    # 2. Prendre l'objet k-1
                    recherche(k - 1, mMax - masses[k - 1])
                    choixAvecObjet = dejaVu[(k - 1, mMax - masses[k - 1])] + [1]

                    # Comparer les deux choix et prendre le meilleur
                    prixSansObjet = prixChoix(choixSansObjet)
                    prixAvecObjet = prixChoix(choixAvecObjet)

                    if prixSansObjet >= prixAvecObjet + prix[n - 1]:
                        choixOptimal = choixSansObjet + [0]
                    else:
                        choixOptimal = choixAvecObjet

                # Stocker le choix optimal dans dejaVu
                dejaVu[(k, mMax)] = choixOptimal

    # Nombre d'objets
    n = len(masses)
    # Appeler la fonction de recherche pour résoudre le problème
    recherche(n, masseMax)

    # Retourner la solution optimale pour le sac complet
    return dejaVu[(n, masseMax)]


# Exemple d'utilisation
masses = [2, 3, 4, 5]
prix = [3, 4, 5, 6]
masseMax = 8

print(sac(masses, prix, masseMax))  # Exemple : [0, 0, 1, 1]
