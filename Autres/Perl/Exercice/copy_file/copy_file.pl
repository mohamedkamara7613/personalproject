#!/usr/bin/env perl
use strict;
use warnings;
#--------------------------------------------------------------------------------

my $filename1 = 't1.txt';
my $filename2 = 't2.txt';
my $fh1;
my $fh2;

print("Ouverture de '$filename1'...\n");
open($fh1, '<', $filename1) or die ("Erreur : impossible d'ouvrir le fichier '$filename1'\n");
open($fh2, '>', $filename2) or die ("Erreur : impossible d'ouvrir le fichier '$filename2'\n");

print("Fichier ouvert avec succés !\n");
print("Création de '$filename2'...\n");
print("Fichier créé avec succés !\n");
print("Préparation de la copie...\n");
print("Copie du fichier '$filename1' vers '$filename2'....\n");



while (my $line = <$fh1>)
{
	print $fh2 "$line";
}
print("Fin de la copie !\n");

close $fh2;
close $fh1;
#--------------------------------------------------------------------------------
<>;