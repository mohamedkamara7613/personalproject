#!/bin/bash
#prend en parametre un fichier et affiche le nombre de lignes
nbligne=$(wc -l < $1)
echo $nbligne
