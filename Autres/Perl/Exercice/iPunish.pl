# -------------------- INTRO --------------------------

# Si vous avez une punition à recopier, utilisez-moi.


use strict;
use warnings;
#--------------------------------------------------------------------------------

print("\tEntrez la phrase à recopier : ");
my $phrase = <>;
chomp $phrase;

print("\tCombien de fois : ");
my $fois = <>;
chomp $fois;

my $resultat = "$phrase\n" x $fois;
print("Et voila le travail :\n");
print("$resultat");

#--------------------------------------------------------------------------------
<>;