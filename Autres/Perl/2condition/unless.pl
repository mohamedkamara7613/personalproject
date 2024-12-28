use strict;
use warnings;
#--------------------------------------------------------------------------------

print "Entrez le mot de passe : ";
my $pass = <>;
chomp $pass;

# Quitter À MOINS QUE le mot de passe soit "s'il te plait".
die "Erreur d'authentification" unless $pass eq "s'il te plait";

# alternativement, on aurait pu écrire ceci :

# Quitter SI le mot de passe n'est pas "s'il te plait".
die "Erreur d'authentification" if $pass ne "s'il te plait";

# Suite du programme
print "Bienvenue\n";print "Accès autorisé.\n";
print "Bienvenue.\n";
# ... suite du programme
#--------------------------------------------------------------------------------
<>;