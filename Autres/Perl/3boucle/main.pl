use strict;
use warnings;
#--------------------------------------------------------------------------------
my $limite;
my $compteur = 1;

print("Je vais compter les lamas pour m'endormir");
print("Jusqu'à combien dois-je compter ? _: ");
$limite = <>;
chomp $limite;

print("$compteur lamas...\n");

while ($compteur < $limite)
{
	$compteur = $compteur + 1;
	print("$compteur lamas...\n");
}

print("Zzzzzzz.....\n");

#--------------------------------------------------------------------------------
<>;