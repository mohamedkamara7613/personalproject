use strict;
use warnings;
# Affiche le contenu d'un fichier texte en le numérotant
#--------------------------------------------------------------------------------
my $fh;
my $line;

print("Entrez le chemin du fichier texte : ");
my $filename = <>;
chomp $filename;


open($fh, '<', $filename) or die ("Erreur : impossible d'ouvrir le fichier '$filename'");

my $num_line = 1;
while ($line = <$fh>)
{
	print("$num_line: \t$line");
	$num_line++;
}
print "\n";

close $fh;
#--------------------------------------------------------------------------------
<>;