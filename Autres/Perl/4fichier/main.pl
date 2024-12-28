use strict;
use warnings;
#--------------------------------------------------------------------------------
# Chemin du fichier à ouvrir en écriture.
# my $filename = "C:\\fichier_test.txt"; # Sous Windows
my $filename = "/home/arnaud/fichier_test.txt"; # Sous Linux
my $fh;

open ($fh, '>', $filename) or die "Impossible d'ouvrir le fichier $filename en écriture";
# ... code qui écrit dans le fichier ...
close $fh;


open ($fh, '<', $filename) or die "Impossible d'ouvrir le fichier $filename en lecture";
# ... code qui lit le fichier ...
close $fh;


# >> ajout dans le fichier

# ou utiliser difined pour verifier si la variable fh est definie ou pas 
#--------------------------------------------------------------------------------
#---------ECRITURE DANS UN FICHIER -------------------------------
open (my $fh, '>', 'fichier_test.txt') or die "Impossible d'ouvrirle fichier";

print $fh "Hello, World !\n"; # On précise à la fonction print le
							  # filehandle dans lequel on désire écrire

close $fh;

#--------------------------------------------------------------------------------
# -------------LECTURE DANS UN FICHIER ---------------------------------------
<>;