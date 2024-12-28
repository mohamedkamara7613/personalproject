use strict;
use warnings;
#--------------------------------------------------------------------------------

print("Etes-vous un homme ou une femme ? Tapez H ou F  _: ");
my $saisie = <>;
chomp $saisie;

if ($saisie eq 'H' or $saisie eq 'h' )
{
	print("Bonjour, monsieur");
}
elsif ($saisie eq 'F' or $saisie eq 'f')
{
	print("Bonjour, madame");
}
else
{
	print("Donc qu'est ce que vous êtes !!!!");
}
#--------------------------------------------------------------------------------
<>;