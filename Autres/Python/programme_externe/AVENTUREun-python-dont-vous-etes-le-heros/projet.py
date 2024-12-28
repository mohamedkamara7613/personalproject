#DEBUT
_deb= "BIENVENUE DANS "
_deb2 ="UN PYTHON DONT VOUS ETES LE HEROS"
_deb3 = "Pour commencer appuyez sur A"
centre = _deb.center(200)
centre1 = _deb2.center(200)
centre2=_deb3.center(200)
print(centre)
print(end='\n')
print(centre1)                                                                                    
print(end='\n')
print(centre2)
deb =input()
if deb != "a" :
    while deb != "a":
        deb =input()   
        if deb == "a":
            réponse = input("quel est votre nom?") 
            break
else :
    réponse = input("quel est votre nom?") 

#MODULE
import json
import time
import random
import sys
#VARIABLE
argent = 100
bouclier = 1
rien = "".strip()
autre_lettre = "motdepasse"
variable = ""
codetriche = 1
magicien = 0
blessure = 0
allumette = 0
combat = 0
fin = 0
coup = 0
monstre = 0
#FONCTION
def temps (sec):
    time.sleep(sec)
def quitte():
    temps(3)
    exi = input("Appuyez sur (a) pour quitter")
    if exi != "a" :
        while exi != "a":
                exi =input()   
                if exi == "a":
                    sys.exit()
    else :
        sys.exit()

def dés(chiffre1,chiffre2,nombre,phrase,phrase1):
    print("Vous lancez le dés")
    print("...")
    temps(0.5)
    print("...")
    temps(0.5)
    print("...")
    temps(0.5)
    chiffre = random.randint((chiffre1),(chiffre2))
    print("Vous avez fait {ch}".format(ch = chiffre))
    if chiffre<= (nombre):
        temps(1)
        print(phrase)
        temps(2)
        print(mort)
        quitte ()
        sys.exit()
    else:
        temps(1)
        print(phrase1)

def énigme(rep = autre_lettre,rep1 = autre_lettre,rep2 = autre_lettre,rep3 = autre_lettre,rep4 = autre_lettre,rep5 = autre_lettre,rep6 = autre_lettre,rep7 = autre_lettre,rep8 = autre_lettre,rep9 = autre_lettre,rep10 = autre_lettre,rep11=autre_lettre):
    global var
    if enig == (rep):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep1):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep2):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep3):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep4):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep5):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep6):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep7):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep8):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep9):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep10):
        print("BONNE REPONSE!")
        var = 1
    elif enig == (rep11):
        print("BONNE REPONSE!")
        var = 1
    else:
        print("MAUVAISE REPONSE")
        var = 0
def program(choixa = "a", choixb = "b", choixc = "c",dem = rien,dem1 = rien, dem2 = rien, dem3 = rien,répa1 = rien, répa2 = rien, répa3 = rien, répa4 = rien, répa5 = rien,répb1 = rien, répb2 = rien, répb3 = rien, répb4 = rien, répb5 = rien,répc1 = rien, répc2 = rien, répc3 = rien, répc4 = rien, répc5 = rien,si = rien, si1 = autre_lettre,si2 = rien):
    print(dem)
    temps(0.5)
    print(dem1)
    temps(0.5)
    print(dem2)
    temps(0.5)
    print(dem3)
    global touche
    global choix
    touche = input()
    while touche !=  (choixa) or (choixb) or (choixc):
        if  touche == (choixa) :
            print(répa1)
            temps(1)
            print(répa2)
            temps(1)
            print(répa3)
            temps(1)
            choix = 0
            if (si) == (si1):
                print(si2)
                break
            else:
                print(répa4)
                temps(1)
                print(répa5)
                break
        elif touche == (choixb):
            print(répb1)
            temps(1)
            print(répb2)
            temps(1)
            print(répb3)
            temps(1)
            print(répb4)
            temps(1)
            print(répb5)
            choix = 1
            break
        elif touche == (choixc):
            print(répc1)
            temps(1)
            print(répc2)
            temps(1)
            print(répc3)
            temps(1)
            print(répc4)
            temps(1)
            print(répc5)
            choix = 2
            break
        elif touche != (choixa) or (choixb) or (choixc):
            print(dem)
            temps(0.5)
            print(dem1)
            temps(0.5)
            print(dem2)
            temps(0.5)
            print(dem3)
            touche = input()

def program_over():
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        print("..........")
        temps(1)
        print("finit (-_-)")
        print("merci d'avoir participer à cette aventure, ceci est test pour m'exercer que j'ai crée en python")
        quitte()
        
def crédit():
    print("CREDIT".center(200))
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    print("CREATEUR:".center(200))
    temps(1)
    print("")
    print("ROMAIN".center(200))
    temps(1)
    print("")
    print("")
    print("RESPONSABLE:".center(200))
    temps(1)
    print("")
    temps(1)
    print("ROMAIN".center(200))
    print("")
    print("")
    temps(1)
    print("RESPONSABLE MARKETING:".center(200))
    temps(1)
    print("")
    print("ROMAIN".center(200))
    temps(1)
    print("")
    print("")
    temps(1)
    print("TESTEUR:".center(200))
    temps(1)
    print("")
    temps(1)
    print("ROMAIN".center(200))
    print("")
    temps(1)
    print("ORANE".center(200))
    print("")
    temps(1)
    print("CAMIlLLE".center(200))
    print("")
    temps(1)
    print("JEAN".center(200))
    print("")
    temps(1)
    print("LAURENCE".center(200))

    temps(2)
    print("")
    print("")
    temps(1)
    print("CE PROJET A PUT ETRE REALISEZ GRACE A LA PARTICIPATION DE:".center(200))
    temps(1)
    print("")
    temps(1)
    print("ROMAIN".center(200))
    print("")
    print("")
    temps(1)
    print("REMERCIMENT A:".center(200))
    temps(1)
    print("")
    print("ROMAIN".center(200))
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    print("")
    temps(1)
    print("MERCI D'AVOIR JOUER A MON JEU".center(200))

    print("")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
    print("..........................................................................................................................................................................................................................................................................................................................................................................................................")
    temps(1)
#VARIABLE TEXTE
mort = """Malheureusement vous étes morts. Ainsi s'achève votre aventure, mais restez en paix,
le prochain aventurier sera peut étre celui qui réussira cette périlleuse mission""" 
phrase_intro = """Bonjour {aventurier}, vous avez décidé de venir dans la ville de Crajkan pour affronter un terrible
monstre du nom de Kroll.""".format(aventurier = réponse)
phrase_intro1 = """Si vous réussissez à le tuer vous aurez droit à une grosse somme d'argent."""
phrase_intro2 = """Vous devrez battre beaucoup de monstres et bien sur faire les bons choix pour réussir.
Bon courage!!"""
nb = """vous avez {argent} pièce d'or, un bouclier, une épée et bien sur le sortilège pour
vous aider quand vous serez face à kroll""".format(argent = argent)
nb1 = """: ALAKAZAM BRADAM VADAM.
Souvenez vous en bien, vous devrez le réciter une fois devant Kroll."""
questionuser = "Si vous étes préts, appuyer sur A"
questionuser1 = "Quand vous serez préts, appuyer sur A"
grotte  = """vous rentrez dans une grotte avec des murs lisses et au moment ou vous rentrez la
porte se referme derrière vous."""
grotte1 = "Vous étes plongés dans le noir et coincés dans la grotte!"
question = "Que voulez vous faire ,{aventurier}?".format(aventurier=réponse)
question_grotteA ="-Examiner le mur devant vous (a)"
question_grotteB = "-Essayer de forcer le mur derrière vous avec votre bouclier pour sortir de cette grotte(b)"
question_grotteC ="-Ne rien faire et attendre(c)"
réponse_grotteA = "Vous examinez le mur quand votre doigt touche un trou dans le mur."
réponse_grotteA1 = """Vous appuyez dessus et une porte menant sur un couloir s'ouvre en grincant.
Vous avancez tout droit."""
réponse_grotteA2 = """Vous marchez le long d’un grand couloir quand vous arriver à une intersection."""
réponse_grotteB = """vous foncez sur le mur derrière vous, bouclier en avant, mais malheureusement
il éclate en mille morceau."""
réponse_grotteB1 = "Vous n'avez plus de bouclier désormais! Il vous reste deux autres choix."
réponse_grotteC = """Vous vous allongez sur le sol et vous vous endormez. Vous vous réveillez en sursaut à
cause d'un bruit grincant"""
réponse_grotteC1 = """Un mur face à vous s'ouvre et un nain en sort. Il vous demande 100 pièces d'or(toutes vos pièces d'or!) ou sinon la mort"""
test = "ceci est un teste"
question_alterA = "-voulez vous prendre à droite?(a)"
question_alterB = "-ou à gauche?(b)"
question_grotte_nainA = "-Voulez-vous donnez les pièces d'or au nain?(a)"
question_grotte_nainB = "-Ou bien le combattre?(b)"
réponse_alterA = """Vous marchez depuis un petit moment quand un Troll gigantesque barre le passage en
étant assis en plein millieu"""
réponse_alterB = "Vous marchez depuis un petit moment quand vous arrivez devants 3 portes."
réponse_alterB1= """La première à une pancarte avec une étoile rouge,
la deuxième une étoile bleu et la troisième une étoile verte."""
réponse_grotte_nainA = "Vous lui donnez 100 pièces d'or et il vous laissent partir"
réponse_grotte_nainB = """Vous sortez votre épée mais avant méme que vous attaquiez,
il crie ALAKAZOUM et vous réduit en poussière."""
question_trollA = "-Voulez-vous le combattre?(a)"
question_trollB = "-Le réveiller?(b)"
question_trollC = "-Ou rebrousser chemin?(c)"
réponse_trollA = "Vous avez donc décider de le combattre, un choix courageux."
réponse_trollA1 = """Vous dégainer votre épé et la planter dans son ventre. Il lève sa massue et l’envoie sur votre
flan droit."""
réponse_troll_bouclier ="""Malheureusement, vous n'avez plus de bouclier et sa massue vous broie
le ventre et vous mourrez dans d'atroce souffrance"""
réponse_trollA2 = """Vous parez le coup avec votre bouclier et il explose en milles morceaux. Vous
en profitez pour planter votre lame dans son coeur."""
réponse_trollB = """Vous secouez délicatement le monstre quand il se réveille en hurlant et n'a pas
l'air de vous vouloir du bien"""
dés_malheureux = "Malheureusement ce n'est pas assez, le troll dans son dernier souffle à encore assez de force pour vous fracassez votre téte avec sa massue, dommage, il aurait fallu le poignarder plus fort."
dés_heureux = "Vous le tuez sur le coup et il s'éffondre sur le sol"
question_fioleA = "-Voulez vous boire la fiole?(a)"
question_fioleB = "-Ou la laissez là et continuer votre chemin?(b)"
réponse_fioleA = "Vous buvez la fiole et votre vision commence à devenir trouble. Vous allez mourir !"
réponse_fioleA1 = "Dans vos derniers instants vous pensez que vous ne parviendrais jamais a tuer kroll. Vous vous réveillez. Vous croyants dans l’au delas, vous vous redressez."
réponse_fioleA2 = "Vous n’étes pas mort et vous étes désormais un magicien ! Vous pouvez désormais réduire en poussière vos ennemis avec une simple formule magique!"
réponse_fioleA3 = "Vous continuez votre chemin"
question_porteA = "-Ouvrir la porte avec l'étoile rouge?(a)"
question_porteB = "-Celle avec l'étoile bleu?(b)"
question_porteC = "-Ou encore celle avec l'étoile verte?(c)"
réponse_porteABC = "Vous entrez et la porte se ferme toute seule derrière vous."
réponse_porteA = "Un squelette vous fait face, armé d'un bouclier et d'une épée, et derrière lui se trouve la porte pour sortir"
réponse_porteB = "Une veille dame vous regarde et derrière elle se trouve la porte pour sortir."
réponse_porteC = "De l'autre cotés de la pièce il y a une porte pour sortir et devans vous une table avec une boite posé dessus."
question_porte_rougeA = "-Voulez-vous le combattre?(a)"
question_porte_rougeB = "-Ou bien essayer de le contournez en vitesse pour passez par la porte derrière lui?(b)"
réponse_porte_rougeA = "Vous vous approchez et il se met à bouger et fonce sur vous, l'épée en avant"
réponse_porte_rouge_magicienA = "Mais heureusement vous ètes un magicien!"
réponse_porte_rouge_magicienA1 = "Vous criez ALAKAZOUM et réduisez votre adversaire en cendre"
réponse_porte_rougeA1 = "Vous sortez votre épée et commencez à combattre"
réponse_porte_rougeA2 = "Il tente un assaut et vous essayer d'esquivez"
dés_malheureux1 = "Vous tentez d'esquivez mais malheureusement vous n'avez pas était assez rapide, il vous coupe en deux et vous mourrez dans d'atroce souffrance."
dés_heureux1 = "Vous réussissez à esquiver et lui tranchez la téte"
réponse_porte_rougeB = "Vous le contournez mais au moment ou vous ouvrez la porte il vous tranche en deux et vous mourrez dans d'atroce souffance."
question_squeletteA = "-Voulez-vous l'examiner?(a)"
question_squeletteB = "-Ou bien continuez votre chemin?(b)"
réponse_squeletteA = "Vous vous baissez pour examiner son cadavre quand il se redresse et plante son épée dans votre jambe."
réponse_squeletteA1 = "C’est un squelette, il ne peut pas mourir."
réponse_squeletteA2 = "Vous le réduisez néanmoins en morceau pour étre sur qu’il ne vous causera pas d’autre problème."
réponse_squeletteA3 = "Votre blessure a la jambe vous fait très mal mais vous continuez quand méme."
question_porte_bleuA = "-Voulez-vous l'attaquez?(a)"
question_porte_bleuB = "-Lui dire bonjour?(b)"
question_porte_bleuC= "-Ou bien sortir par la porte d'en face?(c)"
réponse_porte_bleuA = "Vous l'attaquez l'épée en avant, mais avant que vous faites un pas elle crie ALAKAZOUM et vous réduit en cendre."
réponse_porte_bleuB = "Vous lui dites bonjour et elle se met à vous parler."
réponse_porte_bleuC = "Vous essayer de passez par la porte mais elle est fermée."
réponse_porte_bleuC1 = "C'est alors que la veille dame se retourne et se met à vous parler."
réponse_porte_bleu = """Elle vous dit: "je vais vous poser une énigme, si vous répondez juste vous pourrez passez sinon vous mourrez"""
question_sorcière = "-Ou bien répondre à son énigme(b)"
réponse_sorcière = "(énigme) "
liste = ["""Je ne respire jamais mais j'ai beaucoup de souffle
Qui suis-je?  (""",
"Qu'est ce qui est plus grand que la Tour Eiffel, mais infiniment moins lourd ?",
"""J’ai 1000 frère et chacun en a 1000.
Combien nous sommes ? """ ,
"""Aussitôt que l’on me nomme, je n’existe plus.
Qui suis-je ?""",
"Qu’est-ce qui est né grand, et qui meurt petit ?"]
énigme_heureux= "Bravo, vous avez bien répondu à mon énigme."
énigme_heureux1="ça faisait tellement longtemps qu'on n'avait pas répondut juste à mon énigme que je vous offre cette alumette de magie"
énigme_malheureux="hahahahahahahhaahahaaaaaa vous avez faut"
énigme_malheureux1="En une fraction de seconde elle vous arrache la téte et la mange"
question_porte_vertA = "-Voulez-vous ouvrir la boite posée sur la table?(a)"
question_porte_vertB = "-Ou bien sortir par la porte d'en face?(b)"
réponse_porte_vertA=""""Un serpent en sort et vous mort. Il s’agit d’un venin mortel,
vous n’avez plus que quelque minute a vivre avant de mourir dans d’atroce souffrance."""
consigne ="(faites attention à ne pas mettre d'espace avant et après votre réponse et d'écrire le mot dans la bonne orthographe)"
salle_Kroll="Vous passez la porte et vous rentrez dans une immense salle."
salle_Kroll1=" Au centre, une pierre précieuse bleu et une autre verte."
salle_Kroll2="""L’une d’entre elle vous feras mourir dans d’atroce souffrance dés que vous la toucherai,
l’autre invoquera KROLL et vous pourrez enfin le combattre et libérer le pays de ce tyran si vous arrivez à le battre."""
question_salleA= "-Prendre la pierre verte(a)"
question_salleB="-Ou la pierre bleu(b)"
question_salle="""-En étes vous sur?(a),
-pour retournez en arrière(autre touche)"""
réponse_salleA = "Vous touchez la pierre et… il ne se passe rien.Ouf!"
réponse_salleA1="Votre soulagement est de courte durée car devans vous apparaît KROLL."
réponse_salleB="Votre bras commence a vous sembler lourd, puis il commence à devenir violet."
réponse_salleB1="Cela commence à se propager dans tout votre corps et vous vous tordez de douleur. "
réponse_salleB2="Après 1h de la pire douleur jamais ressenti, vous arrétez enfin d’agoniser, vous étes mort ce qui est un réel soulagement pour vous."
combat_finale = "Votre combat contre KROLL commence."
combat_finale1 = "Vous aviez appris une formule pour vous aidez contre lui."
question_combat = "Est-ce?"
question_combatA = "-ALAKAZOUM BRADAM VADAM(a)"
question_combatB = "-ALAKAZAM BRADAM VADAM(b)"
question_combatC = "-ALAKAZAM BRADOUM VADOUM(c)"
réponse_combatB = "Vous récitez la formule et KROLL se tord de douleur. La formule a marcher !"
réponse_combatB1 = "Il est maintenant qu’a 50 % de sa force."
réponse_combatB2 = "Il envoie sa hache sur vous en hurlant de rage"
réponse_combatAC = "Vous récitez la formule mais rien ne se passe."
réponse_combatAC1 = "KROLL s’avance vers vous en ricanant et vous déchiqute en morceau de manière a vous faire le plus mal possible."
combat_bouclier= "Vous contrez sa hache avec votre bouclier qui éclate en mille morceaux"
combat_nbouclier = "Vous n'avez pas de bouclier! Vous tentez d'esquivez mais sa hache vous touche quand méme et vous commencez à perdre beaucoup de sang"
combat_nbouclier_bless= "Eyant déja perdu beaucoup de sang à cause de votre blessure à la jambe, vous vous évanouissez ce qui signifie la fin de l'aventure pour vous car Kroll ne va pas attendre que vous vous réveillez"
dés_malheureux2 = "La blessure est trop profonde, vous perdez trop de sang et vous vous évanouissez ce qui signifie la fin de l'aventure pour vous car Kroll ne va pas attendre que vous vous réveillez"
dés_heureux2= "Heureusement pour vous, la blessure est peu profonde et vous pouvez continuez le combat"
blessure_ =  "pour savoir si la blessure ne vous tue pas"
début_combat = "Le vrai combat contre Kroll commence!"
combat_magie= "Fort heureusement, vous étes un magicien gràce à la fiole que vous aviez but"
combat_magie1 = "Vous criez ALAKAZOUM et affaiblissez encore davantage Kroll, la victoire est proche!"
question_allumette = """Vous avez une allumette de magie que vous aviez donné la sorcière.
-Voulez vous l'utilisez?(a),
-ou non (n'importe quelle touche)?"""
réponse_nallumette="Vous n'utilisez pas votre allumette, dommage, vous étes vraiment bète, vous auriez put gagner"
gagner_allumette = "Vous utilisez votre allumette et Kroll titube et s'éffondre par terre."
assaut1 = "Vous tentez l'assaut finale et maintenant que kroll, étonnés que vous ayez survécu à sa hache, est désarmais, vous lui enfoncez de toutes vos forces votre épée dans son ventre"
dés_malheureux3= "Vous prenez votre épée et l’enfoncez de toute vos forces dans le corps de KROLL. Malheureusement il est trop puissant et votre épée éclate en mille morceau."
dés_heureux3="Vous prenez votre épée et l’enfoncez de toute vos forces dans le corps de KROLL. Surpris, il titube, déjà affaibli par votre formule magique. Vous en profitez pour lui coupez la téte."
gagner_allumette2="Vous utilisez votre allumette et Kroll titube."
gagner = "FELICITATION,{name}  VOUS AVEZ VAINCU KROLL!!!".format(name = réponse.upper())
gagner1 = "Vous serez le héros national quand les gens seront que vous avez débarassez le pays de ce tyran!"
gagner2 = "Derrière le corps de KROLL se trouve une porte, probablement la sortie"
gagner3= "Néanmoins si vous n'étes pas confiant vous pouvez faire tous le chemin arrière jusqu'a revenir à l'endroit ou vous étes arrivez"
fiole_ ="Vous trouvez sur son corps une fiole rempli d'un liquide bleu"
question_gagnerA= "-Prendre la porte derrière le cadavre de Kroll(a)"
question_gagnerB="-refaire tous le chemin en sens inverse(b)"
réponse_gagnerA="Vous sortez de la montagne et les habitants vous aclament !"
réponse_gagnerA1="Vous gagner une montagne d’argent, vous étes un des hommes les plus riches du pays et bien sur vous avez la gloire d’avoir débarrassez le pays du tyran KROLL."
réponse_gagnerA2="Néanmoins, votre heure de gloire sera courte car le roi jaloux de votre succès engagea quelqu’un pour mettre du poison dans votre verre."
réponse_gagnerA3="Vous mourrez dans votre someil, en ne vous rendant comte de rien mais vous mourrez heureux."
réponse_gagnerB = "Vous revenez sur vos pas et vous marchez déjà depuis 15 minutes quand vous avez l’impression d’étre déjà passé par la."
réponse_gagnerB1= "Vous étes perdu car cette montagne est un vaste labyrinthe, et vous resterez à jamais dans cette montagne avec la honte d’avoir battu Kroll mais de s’étre lamentablement perdu"
réponse_gagnerB2="Vous mourrez de faim dans quelque jour et vous ne serez plus qu’un squelette dans quelque semaine."
question_paramétre = "Appuyez sur A pour accédez aux paramètre de votre avanture"
question_crédit = "Appuyez sur B pour accédez au crédit de ce PYTHON DONT VOUS ETES LE HEROS(®tout droit réservé)"
question_quitter = "Appuyez sur Z pour quitter"
#DEROULEMENT
# program = un programme modulable qui pose la question et en fonction du choix fournit une
#réponse. On peut moduler le nombre de choix (maximum3) avec:
#les arguments: choixa, choixb,choixc. Suivant le choix de touche qu'on veut supprimer on écrit
#par exemple : choix tel lettre = autre_lettre.

#On peut aussi moduler les demandes (maximum4) avec:
#les arguments: dem, dem1, dem2, dem3. on ecrit par exemple dem = tel phrase.

#On peut enfin moduler les réponses de chaque touche (maximum5 par touches) avec:
#les arguments: répa1,répa2,répa3,répa4,répa5,   répb1,répb2,répb3,répb4,répb5,   répc1,répc2,répc3,répc4,répc5

#module de variable: on peut spécifier si tel variable = tel nombre dire tel phrase. Les arguments:
#si = variable, si1 = chiffre, si2 =  phrase à dire.


#dés = pour dire vous lancez le dés, (attente) si le chiffre entre tel et tel est supérieur au chiffre demandé,
#dire une phrase et quitte le programme, sinon dit une autre phrase.
#Les arguments: chiffre1 = entre minimum chiffre, chiffre2 = et maximum chiffre.nombre,phrase,phrase1
#nombre = chiffre demandé ou il faut avoir ce chiffre ou supérieur pour gagner
#phrase = phrase dite si on perd
#phrase1 = phrase dite si on gagne

#énigme= pour avoir plusieurs possiblilité de mots, jusqu'a 11(rep,rep1,rep2... jusqu"a rep11
print(phrase_intro )
temps(0.5)
print(phrase_intro1)
temps(0.5)
print(phrase_intro2)
temps(0.5)
touche = input(questionuser)
    
if touche != "a" :
    while touche != "a":
        touche = input(questionuser1)      
        if touche == "a":
            print(nb)
else :
    temps(1)
    print(nb)

temps(0.5)
print(nb1)
temps(2)
print(grotte)
temps(1)
print(grotte1)
temps(0.5)

#1er partie
while codetriche == 1:
    program(dem = question, dem1 = question_grotteA, dem2 = question_grotteB, dem3 = question_grotteC, répa1 = réponse_grotteA, répa2 = réponse_grotteA1,répa5=réponse_grotteA2,répb1 = réponse_grotteB, répb2 = réponse_grotteB1,répc1 = réponse_grotteC,répc2 = réponse_grotteC1 )
    #si c'est A
    if choix == 0:
        program(choixc=autre_lettre,dem=question,dem1=question_alterA,dem2=question_alterB,répa1=réponse_alterA,répb1=réponse_alterB,répb2=réponse_alterB1)
        coup = coup+1
        if touche == "a":
            variable = 0
            coup = coup+1
            break
        elif touche == "b":
            variable = 1
            coup = coup+1
            break
            
    #si c'est B
    elif choix == 1:
        program(choixb=autre_lettre,dem = question, dem1 = question_grotteA, dem3 = question_grotteC, répa1 = réponse_grotteA, répa2 = réponse_grotteA1,répa5=réponse_grotteA2,répc1 = réponse_grotteC,répc2 = réponse_grotteC1)
        bouclier = 0
        coup = coup+1
        #si c'est A dans B
        if choix == 0:
            program(choixc=autre_lettre,dem=question,dem1=question_alterA,dem2=question_alterB,répa1=réponse_alterA,répb1=réponse_alterB,répb2=réponse_alterB1)
            coup = coup+1
            if touche == "a":
                variable = 0
                coup = coup+1
                break
            elif touche == "b":
                variable = 1
                coup = coup+1
                break
        #si c'est C dans B
        elif choix ==2:
            program(choixc = autre_lettre,dem=question,dem1=question_grotte_nainA,dem2=question_grotte_nainB,répa1=réponse_grotte_nainA,répb1=réponse_grotte_nainB,répb5=mort)
            coup = coup+1
            argent = 0
            if touche =="b":
                quitte()
                break
            else:
                program(choixc=autre_lettre,dem=question,dem1=question_alterA,dem2=question_alterB,répa1=réponse_alterA,répb1=réponse_alterB,répb2=réponse_alterB1)
                if touche == "a":
                    variable = 0
                    coup = coup+1
                    break
                elif touche == "b":
                    variable = 1
                    coup = coup+1
                    break
    #si c'est C
    elif choix ==2:
        program(choixc = autre_lettre,dem=question,dem1=question_grotte_nainA,dem2=question_grotte_nainB,répa1=réponse_grotte_nainA,répb1=réponse_grotte_nainB,répb5=mort)
        coup = coup+1
        argent = 0
        if touche =="b":
            quitte()
        else:
            program(choixc=autre_lettre,dem=question,dem1=question_alterA,dem2=question_alterB,répa1=réponse_alterA,répb1=réponse_alterB,répb2=réponse_alterB1)
            if touche == "a":
                variable = 0
                coup = coup+1
                break
            elif touche == "b":
                variable = 1
                coup = coup+1
                break

#2eme partie 

#le troll
while codetriche == 1:
    if variable == 0:
        program(dem = question, dem1 = question_trollA,dem2 = question_trollB,dem3 = question_trollC,répa1 = réponse_trollA, répa2 = réponse_trollA1,si = bouclier, si1 = 0, si2 = réponse_troll_bouclier,répa4 = réponse_trollA2,répb1 = réponse_trollB,répc1 = réponse_alterB,répc2 = réponse_alterB1)
        #si combattreA
        if choix == 0:
            coup = coup+1
            monstre = monstre+1
            #si pas de bouclier
            if bouclier == 0:
                temps(2)
                print(mort)
                quitte()
            #si bouclier
            else:
                bouclier = 0
                dés(chiffre1 = 1, chiffre2 = 10,nombre = 5,phrase = dés_malheureux,phrase1 = dés_heureux)
                temps(2)
                print(fiole_)
                program(choixc = autre_lettre,dem = question,dem1 = question_fioleA,dem2 = question_fioleB,répa1 = réponse_fioleA,répa2=réponse_fioleA1,répa3=réponse_fioleA2,répa4=réponse_fioleA3,répa5 = réponse_alterB+réponse_alterB1,répb1=réponse_fioleA3,répb4=réponse_alterB,répb5=réponse_alterB1)
                #si boire la fiole
                if touche =="a":
                    coup = coup+1
                    magicien = 1
                    variable = 1
                    break
                #si pas boire
                else:
                    coup = coup+1
                    variable = 1
                    break
        #si réveillerB
        elif choix==1:
            program(choixb = autre_lettre,dem = question, dem1 = question_trollA,dem2 = question_trollC,répa1 = réponse_trollA, répa2 = réponse_trollA1,si = bouclier, si1 = 0, si2 = réponse_troll_bouclier,répa4 = réponse_trollA2,répc1 = réponse_alterB,répc2 = réponse_alterB1)
            coup = coup+1
            #si le combatA dans B
            if choix == 0:
                monstre = monstre+1
                coup = coup+1
                #si pas de bouclier
                if bouclier == 0:
                    temps(2)
                    print(mort)
                    quitte()
                    break
                #si bouclier
                else:
                    bouclier = 0  
                    dés(chiffre1 = 0, chiffre2 = 10,nombre = 5,phrase = dés_malheureux,phrase1 = dés_heureux)
                    temps(2)
                    print(fiole_)
                    program(choixc = autre_lettre,dem = question,dem1 = question_fioleA,dem2 = question_fioleB,répa1 = réponse_fioleA,répa2=réponse_fioleA1,répa3=réponse_fioleA2,répa4=réponse_fioleA3,répa5 = réponse_alterB+réponse_alterB1,répb1=réponse_fioleA3,répb4=réponse_alterB,répb5=réponse_alterB1)
                    #si boire la fiole
                    if touche =="a":
                        coup = coup+1
                        magicien = 1
                        variable =1
                        break
                    #si pas boire
                    else:
                        variable = 1
                        coup = coup+1
                        break
            #si revient en arrièreC dansB
            elif choix == 2:
                coup = coup+1
                variable = 1
                break
        #si revient en arrièreC
        elif choix == 2:
            coup = coup+1
            variable = 1
            break
    else:
        break

#3eme parties

#les portes 

while codetriche == 1:
    if variable ==1:
        #programme base 3 portes
        program(dem = question,dem1=question_porteA,dem2=question_porteB,dem3=question_porteC,répa1=réponse_porteABC,répa4=réponse_porteA,répb1=réponse_porteABC,répb4=réponse_porteB,répc1=réponse_porteABC,répc4=réponse_porteC)

        #porte rouge
        if choix == 0:
            coup = coup+1
            program(choixc = autre_lettre,dem = question,dem1=question_porte_rougeA,dem2=question_porte_rougeB,si=magicien,si1=1,si2=réponse_porte_rouge_magicienA+réponse_porte_rouge_magicienA1,répa4=réponse_porte_rougeA1,répa5=réponse_porte_rougeA2,répb1=réponse_porte_rougeB)
            #si combat
            if touche == "a":
                monstre = monstre+1
                coup = coup+1
                #si pas magicien
                if magicien ==0:
                    dés(chiffre1 = 1,chiffre2=10,nombre=4,phrase=dés_malheureux1,phrase1=dés_heureux1)
                    temps(2)
                    print("son cadavre au sol,")
                    program(choixc=autre_lettre,dem=question,dem1= question_squeletteA,dem2=question_squeletteB,répa1=réponse_squeletteA,répa2=réponse_squeletteA1,répa3=réponse_squeletteA2,répa4=réponse_squeletteA3)
                    variable = 2                      
                    if touche == "a":
                        blessure = 1
                        coup = coup+1
                        variable =2
                        break
                    elif touche == "b":
                        variable=2
                        coup = coup+1
                        break
                #si magicien
                elif magicien ==1:
                    variable=2
                    break
            #si contournez
            if touche == "b":
                temps(2)
                print(mort)
                quitte()
    #porte bleu
        if choix ==1:
            program(dem=question,dem1=question_porte_bleuA ,dem2=question_porte_bleuB,dem3=question_porte_bleuC,répa1=réponse_porte_bleuA,répb1=réponse_porte_bleuB,répb4=réponse_porte_bleu,répc1=réponse_porte_bleuC,répc2=réponse_porte_bleuC1,répc4=réponse_porte_bleu)
            coup = coup+1
            #si combattre
            if touche =="a":
                print(mort)
                quitte()
            #question énigme
            program(choixc=autre_lettre,dem=question,dem1=question_porte_bleuA,dem2=question_sorcière,répa1=réponse_porte_bleuA,répb1="Son énigme est,")
            coup = coup+1
            #si combattre
            if touche =="a":
                print(mort)
                quitte()

            while codetriche==1:
                coup = coup+1
                #énigme
                chiffre = random.randint(0,4)
                print(chiffre)    
                print(consigne)
                if chiffre == 0:
                    print(liste[0])
                    enig = input()
                    énigme(rep="sèche-cheuveux",rep1="séche-cheuveux",rep2="un séche-cheuveux",rep3="un sèche-cheuveux",rep4="séche cheuveux",rep5="sèche cheuveux",rep6="un séche cheuveux",rep7="un sèche cheuveux",rep8="seche-cheuveux",rep9="un seche-cheuveux",rep10="seche cheuveux",rep11="un seche cheuveux")
                    break
                elif chiffre == 1:
                    print(liste[1])
                    enig = input()
                    énigme(rep="son ombre",rep1="l'ombre",rep2="une ombre",rep3="ombre")
                    break
                elif chiffre == 2:
                    print(liste[2])
                    enig = input()
                    énigme(rep="1001")
                    break
                elif chiffre == 3:
                    print(liste[3])
                    enig = input()
                    énigme(rep="le silence",rep1="silence",rep2="un silence",rep3="le sillence",rep4="sillence",rep5="un sillence")
                    break
                elif chiffre == 4:
                    print(liste[4])
                    enig = input()
                    énigme(rep="une bougie",rep1="la bougie",rep2="bougie",rep3="une bougi",rep4="la bougi",rep5="bougi")
                else:
                    break
            #si juste
            if var==1:
                print("""...
...
...""")
                temps(2)
                print(énigme_heureux)
                temps(1)
                print(énigme_heureux1)
                allumette = 1
                variable = 2
                break
            #si faux
            elif var == 0:
                print("""...
...
...""")               
                temps(2)
                print(énigme_malheureux)
                temps(0.5)
                print(énigme_malheureux1)
                print(mort)
                quitte()

        #porte verte
        if choix ==2:
            coup = coup+1
            program(choixc=autre_lettre,dem=question,dem1=question_porte_vertA,dem2=question_porte_vertB,répa1=réponse_porte_vertA)
            if touche =="a":
                print(mort)
                quitte()
            elif touche =="b":
                variable=2
                coup = coup+1
                break
#salle des 2 pierres
if variable == 2:
    temps(3)
    print(salle_Kroll)
    temps(1)
    print(salle_Kroll1)
    temps(1)
    print(salle_Kroll2)
    temps(2)
    print(question)
    temps(1)
    print(question_salleA)
    temps(1)
    print(question_salleB)
    touche = input()
    while touche !=  "a" or "b" :
        #pierre verte
        if  touche == "a" :
            print(question_salle)
            touche = input()
            if touche == "a":
                coup = coup+1
                combat =1
                temps(1)
                print(réponse_salleA)
                temps(1)
                print(réponse_salleA1)            
                break
            else:
                print(question)
                temps(1)
                print(question_salleA)
                temps(1)
                print(question_salleB)
                touche = input()
        #pierre bleu
        elif touche == "b":
            print(question_salle)
            touche = input()
            if touche =="a":
                print(réponse_salleB)
                temps(1)
                print(réponse_salleB1)
                temps(1)
                print(réponse_salleB2)
                temps(1)
                print(mort)
                quitte()
            else:
                print(question)
                temps(1)
                print(question_salleA)
                temps(1)
                print(question_salleB)
                touche = input()
        elif touche != "a" or "b":
            print(question)
            temps(1)
            print(question_salleA)
            temps(1)
            print(question_salleB)
            touche = input()    

    #COMBAT FINAL

    while codetriche ==1:
        if combat == 1:
            temps(3)
            print(combat_finale)
            temps(0.5)
            print(combat_finale1)
            monstre = monstre +1
            program(dem=question_combat,dem1=question_combatA,dem2=question_combatB,dem3=question_combatC,répa1=réponse_combatAC,répa3=réponse_combatAC1,répb1=réponse_combatB,répb2=réponse_combatB1,répb3=réponse_combatB2,répc1=réponse_combatAC,répc2=réponse_combatAC1)
            #si bonne formule
            if choix == 1:
                coup = coup+1
                #si bouclier
                if bouclier == 1:
                    print(combat_bouclier)
                    combat =2
                    break
                #si pas de bouclier
                elif bouclier == 0:
                    print(combat_nbouclier)
                    temps(0.5)               
                    #si blessure
                    if blessure == 1:
                        print(combat_nbouclier_bless)
                        temps(1)
                        print(mort)
                        quitte()
                    #si pas blessure
                    elif blessure == 0:   
                        print(blessure_)
                        #une chance sur 2
                        dés(chiffre1=1,chiffre2=10,nombre=5,phrase=dés_malheureux2,phrase1=dés_heureux2)
                        combat=2
                        break
            #si mauvaise formule
            else:
                temps(1)
                print(mort)
                quitte()
    #2eme partie du combat
    while codetriche == 1:        
        if combat ==2:
            print(début_combat)
            #si vous étes un magicien
            if magicien == 1:
                temps(2)
                print(combat_magie)
                temps(0.5)
                print(combat_magie1)
                 #si vous avez l'allumette
                if allumette == 1:
                    temps(0.5)
                    print(question_allumette)
                    touche =input()
                     #si vous étes magicien et si vous utilisez allumette
                    if touche == "a":
                        coup = coup+1
                        temps(2)
                        print(gagner_allumette)
                        fin = 1
                        break
                    #si vous l'utilisez pas
                    elif touche != "a":
                        coup = coup+1
                        temps(1)
                        print(réponse_nallumette)
                        temps(1)
                        print(assaut1)
                        dés(chiffre1=1,chiffre2=100,nombre=55,phrase=dés_malheureux3,phrase1=dés_heureux3)
                        fin = 1
                        break
                #si vous étes magicien et que vous avez pas allumette
                elif allumette == 0:
                    temps(1)
                    print(assaut1)
                    dés(chiffre1=1,chiffre2=100,nombre=45,phrase=dés_malheureux3,phrase1=dés_heureux3)
                    fin = 1
                    break
            #si vous étes pas magicien
            elif magicien == 0:
                #si vous étes pas magicien mais que vous avez allumettes
                if allumette == 1:
                    temps(0.5)
                    print(question_allumette)
                    touche = input()
                    #si vous étes pas magicien et si vous utilisez allumette
                    if touche == "a":
                        coup = coup+1
                        temps(2)
                        print(gagner_allumette2)
                        temps(1)
                        print(assaut1)
                        dés(chiffre1=1,chiffre2=100,nombre=35,phrase=dés_malheureux3,phrase1=dés_heureux3)
                        fin = 1
                        break
                    #si vous l'utilisez pas
                    elif touche != "a":
                        coup = coup+1
                        temps(1)
                        print(réponse_nallumette)
                        temps(1)
                        print(assaut1)
                        dés(chiffre1=1,chiffre2=100,nombre=70,phrase=dés_malheureux3,phrase1=dés_heureux3)
                        fin = 1
                        break
    
                #si pas magicien et pas allumette
                elif allumette == 0:
                    temps(1)
                    print(assaut1)
                    temps(1)
                    dés(chiffre1=1,chiffre2=100,nombre=65,phrase=dés_malheureux3,phrase1=dés_heureux3)
                    fin = 1
                    break

if fin == 1:
    temps(4)
    print(gagner)
    temps(0.7)
    print(gagner1)
    temps(0.8)
    print(gagner2)
    temps(0.7)
    print(gagner3)
    temps(0.5)
    program(choixc=autre_lettre,dem=question,dem1=question_gagnerA,dem2=question_gagnerB,répa1=réponse_gagnerA,répa2=réponse_gagnerA1,répa3=réponse_gagnerA2,répa5=réponse_gagnerA3,répb1=réponse_gagnerB,répb4=réponse_gagnerB1,répb5=réponse_gagnerB2)
    if choix== 1:
        temps(2)
        print(mort)
        quitte()


    #fin
    coup = coup+1
    if choix == 0:
        réponse_paramétre = "Vous avez gagner en {nbc} coup, vous avez tués {nb} monstre dont le boss finale, vous avez {argent} piéces d'or,vous avez {nba} allumette, vous étes {nbm} magicien et vous avez failli mourir beacoup de fois.".format(nbc = coup,nb=monstre,argent=argent,nba=allumette,nbm=magicien)
        temps(10)
        program(choixc="z",dem=question,dem1=question_paramétre,dem2=question_crédit,dem3=question_quitter,répa1=réponse_paramétre)
        #paramétre
        if choix ==0:
            temps(3)
            program(choixa=autre_lettre,choixc="z",dem=question,dem2=question_crédit,dem3=question_quitter)
            if choix ==1:
               crédit()
               temps(2)
               program_over()
            elif choix == 2:
                temps(1)
                program_over()
        elif choix ==1:
            temps(3)
            crédit()
            program(choixb=autre_lettre,choixc="z",dem=question,dem1=question_paramétre,dem2=question_quitter,répa1=réponse_paramétre)
            if choix ==0:
                temps(3)
                program_over()
            elif choix ==2:
                temps(1)
                program_over()
        elif choix == 2:
            temps(2)
            program_over()
    elif choix == 1:
        temps(1)
        print(mort)
        quitte()

