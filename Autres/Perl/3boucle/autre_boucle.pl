use strict;
use warnings;
#--------------------------------------------------------------------------------
#------------------BOUCLE FOR ----------------------------------
# Le compteur est initialisé à 0
# On compte jusqu'à ce qu'il soit égal à 30
# Pour le mettre à jour, on incrémente sa valeur de 1
for (my $compteur = 0; $compteur <= 30; $compteur++)
{
	print "$compteur\n";
}



#--------------BOUCLE DO...WHILE...
my $nb_mystere = int (rand 101);
my $essai; # Pas besoin d'initialiser cette variable
# avec une valeur arbitraire.
print "Devinez le nombre mystère.\n";
do
{
	print '> ';
	$essai = <>;
	
	if ($essai < $nb_mystere)
	{
		print "C'est plus.\n";
	}
	elsif ($essai > $nb_mystere)
	{
		print "C'est moins.\n";
	}

}while ($essai != $nb_mystere);

print "Gagné !";



#------------------BOUCLE UNTIL----------------------
print "Devinez le nombre mystère.\n";
# Répéter JUSQU'À CE QUE le joueur ait trouvé le nombre
until ($essai == $nb_mystere)
{
	print '> ';
	$essai = <>;

	if ($essai < $nb_mystere)
	{
		print "C'est plus.\n";
	}
	elsif ($essai > $nb_mystere)
	{
		print "C'est moins.\n";
	}
}
print "Gagné !";

#--------------------------------------------------------------------------------
<>;