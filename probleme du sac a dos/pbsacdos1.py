def sac(masses, prix, masseMax):
    """

    Parameters
    ----------
    masses : list de taille n
        contient la masse des objets.
    prix : list de taille n
        contient le prix des objets.
    masseMax : int
        masse maximale que le sac "peut contenir".

    Returns
    -------
    list
        contenant des 0 et des 1 disant si on prend l'objet k ou non
    """
    # Dictionnaire pour stocker les solutions déjà calculées,
    dejaVu = {}

    # Fonction pour calculer le prix d'un sac (combinaison de choix)
    def prixChoix(choix):  # choix est une liste de 0 ou de 1
        S = 0
        for i in range(0, len(prix)-1):
            S += choix[i] * prix[i]
        return S

     # Fonction de recherche pour déterminer les choix optimaux
    def recherche(k, mMax):
        # Vérifie si la clé (k, mMax) est déjà dans le dictionnaire
        if (k, mMax) not in dejaVu:

             # Cas de base : un seul objet
            if k == 1:
                if masses[0] < mMax:
                    dejaVu[(1, mMax)] = [1]
                else:
                    dejaVu[(1, mMax)] = [0]
            elif masses[k - 1] > mMax:
                # Cas où la masse du dernier objet est supérieure à mMax

                recherche(k - 1, mMax)
                New = dejaVu[(k - 1, mMax)]
                New.append(0)
                dejaVu[(k, mMax)] = New
            else:
                # Cas où l'on peut inclure ou exclure l'objet k-1
                recherche(k - 1, mMax)
                recherche(k - 1, mMax - masses[k - 1])

                # test
                print(k-1, len(prix), len(dejaVu[(k - 1, mMax)]))

                a = prixChoix(dejaVu[(k - 1, mMax)])
                b = prixChoix(dejaVu[(k - 1, mMax - masses[k - 1])])

                if a >= b + prix[k - 1]:
                    New = dejaVu[(k - 1, mMax)]
                    New.append(0)
                else:
                    New = dejaVu[(k - 1, mMax - masses[k - 1])]
                    New.append(1)

                dejaVu[(k, mMax)] = New

     # Nombre d'objes
    n = len(masses)
    # Appel de la foncion recherche pour les n objets et la masse maximal donnée
    recherche(n, masseMax)

    # Retourne la liste de choix pour le sac optimal
    return dejaVu[(n, masseMax)]


# # Exemples

masses = [2, 3, 4]
prix = [3, 4, 5]
masseMax = 5

print(sac(masses, prix, masseMax))  # sensé retourné 1,1
