use strict;
use warnings;

#--------------------------------------------------------------------------------
# Longueur d'une chaine
my $texte = "Voici un texte";
my $longueur = length $texte;

print("la longueur de la chaine : \"$texte\" est $longueur\n");


# Répétion et concaténation
$texte = "bla" x 10;
print("$texte...\n");

$texte = "cool" . "ympique";
print("$texte\n");

print ('tro' . 'lol' x 10);

print '-' x 10
#--------------------------------------------------------------------------------
<>;