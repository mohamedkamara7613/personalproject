use strict;
use warnings;
#--------------------------------------------------------------------------------

my $a = 2;
my $b = 4;
# La fonction "int" permet de convertir explicitement un scalaire
# en un nombre entier.

print ("$a < $b : " . int($a < $b) . "\n");
print("-----------------------------------------------------\n");

# 0 ou "0" ou "" = faux et tout autres nombres  = vrai

# -----------Pour les nombres ------------------
# == : egale
# < et > : inférieur et supérieur et >= et <= aussi
# != : différent de 


# ----------- Pour les chaines ------------------
# compare lexicographiquement les chaines de caracteres
# eq : égale
# ne : n'est pas égale à
# lt et gt : plus petit que et plus grand que
# le et ge : plus petit ou égale et plus grand ou égale

# --------------- Différent----------------------
# ! : signifie  différent de ...


# ---------------------- OU ---------------------
# '||' ou 'or' : les deux marches

# ---------------------- ET ----------------------
# '&&' ou 'and' : les deux marches

# --------------------- OUBIEN -------------------
# l'un oubien l'autre mais pas les deux en meme temps
# 'xor'

# ---------------- DEFINED ET UNDEF --------------
my $var; # déclaré mais pas définie
print("defined \$var : " . int(defined $var) . "\n");

$var = 42; # $var est maintenant définie
print("defined \$var : " . int(defined $var) . "\n");

$var = undef; # $var n'est plus définie
print("\t\$var = undef \n");
print("defined \$var : " . int(defined $var) . "\n");

print("-----------------------------------------------------\n");
# -----------------EXEMPLE ------------------------
my $error = "\$var n'est pas définie";
my $var;

defined $var && print("\$var = $var\n") or print ("$error\n");

$var = 45;

defined $var && print("\$var = $var\n") or print ("$error\n");

$var = undef;

# vrai ET vrai on affiche si faux on passe à OU 
defined $var && print("\$var = $var\n") or print ("$error\n");

#--------------------------------------------------------------------------------
<>;