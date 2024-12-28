

# Creation d'un sac ayant le nombre de plae
def genere_sac(objets):
    # creer un sac de la bonne taille
    sac = []
    for i in range(len(objets)):
        sac.append(True)

    return sac


def trier_liste(objets):
    """trie la liste d'object en fonction du prix"""
    n = len(objets)
    for i in range(1, n):
        k = objets[i] # prix
        j = i-1 # indice
        while j >= 0 and objets[j][0] > k[0]:
            objets[j+1] = objets[j]
            j -= 1
        objets[j+1] = k
    return objets

def prix_ou_masse_de(sac, objets, choix="prix"):
    choix_total = 0
    for i in range(len(sac)):
        if sac[i]:
            if choix == "prix":
                choix_total += objets[i][0]
            elif choix == "masse":
                choix_total += objets[i][1]
    return choix_total


def recherche_sans_memoisation(k, masse_max):
    """recherche de la meilleure combinaison de objets sans memoisation"""
    pass


def recherche_avec_memoisation(k, masse_max):
    """recherche de la meilleure combinaison de objets avec memoisation"""
    memo = {}
    def recherche(k, masse_max, sac):
       if (k, masse_max) not in memo:
            if k == 1:
                if objets[0][1] <= masse_max:
                    memo[(k, masse_max)] = [True] #objets[0][0]
                else:
                    memo[(k, masse_max)] = [False]
            if prix_ou_masse_de():
                pass
                    





# peut etre representé par un dictionnaire aussi
objets = [(20, 25), (13, 16)]
masse_max = 100

sac = genere_sac(objets)






