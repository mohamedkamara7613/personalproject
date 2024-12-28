use strict;
use warnings;
#--------------------------------------------------------------------------------

my $pass = "vrai";
my $acces = 0;

print("Entrez le mot de passe : ");
my $saisie = <>;
chomp $saisie;

$acces = $saisie eq $pass;

print(" Accés : " . int($acces));

#--------------------------------------------------------------------------------
<>;