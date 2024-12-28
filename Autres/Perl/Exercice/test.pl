use strict;
use warnings;
my $filename = "test";

open (my $fh, '<', $filename) or die "Erreur : impossible d'ouvrir le fichier '$filename'";

# Vous prendrez bien une petite tasse de magie noire ?
while(<$fh>)
{
	print;
}

close $fh;