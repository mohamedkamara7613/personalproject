use strict;
use warnings;
#--------------------------------------------------------------------------------
my $essai = 5;
my $nombre_inconnu = int(rand 21);

print("\tEntrez un nombre 0 et 20.\n");

my $compteur = 0; 
while ($compteur < $essai)
{
	print("-" x 30 . "Vous avez ", $essai - $compteur, " essais" . "-" x 30 . "\n");

	print("\t_: ");
	my $essai_user = <>;
	chomp $essai_user;

	if ($essai_user lt $nombre_inconnu)
	{
		print("\tPlus grand\n");
	}
	elsif ($essai_user gt $nombre_inconnu)
	{
		print("\tPlus petit\n");
	}
	elsif ($essai_user eq $nombre_inconnu)
	{
		print("/" x 20 ." Vous avez reussi " . "\\" x 20 . "\n");
		print("/" x 20 . " le nombre inconnu est bien $nombre_inconnu\n");
		exit(0);
	}

	$compteur++;
}

print("/" x 20 ." PERDU ! UNE PROCHAINE FOIS " . "\\" x 20 . "\n");

	
#--------------------------------------------------------------------------------
<>;