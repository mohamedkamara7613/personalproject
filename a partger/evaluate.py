IA_PLAYER=1
HUMAN_PLAYER=2
def evaluate(board,nb_stimulation):
    #évalue une position donnée en fonction de plusieurs stimulations
    nb_null=0
    nb_victoire_joueur1=0
    nb_victoire_joueur2=0
    for i in range (0,nb_stimulation):
        if simulation(board, IA_PLAYER)==IA_PLAYER:
            nb_victoire_joueur1+=1
        elif simulation( board, HUMAN_PLAYER)==HUMAN_PLAYER:
            nb_victoire_joueur2+=1
        else:
            nb_null+=1
    return (nb_null, nb_victoire_joueur1, nb_victoire_joueur2)


