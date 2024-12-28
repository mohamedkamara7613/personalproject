#!/bin/bash

if [ $# -ge 1 ]
then
	if [ $1 = '--help' ]
	then
		echo -e " \timport_fav <nom_fichier.txt>"
		echo -e " \tLancer le script 'import_fav' en lui envoyant comme paramètre le nom du fichier "
		echo -e " \tqui contient les liens a ouvrir. De préférence ecrivez tous les liens sur une"
		echo -e " \tmeme ligne dans le fichier sinon tous les onglets ne s'ouvriront pas en meme temps"
		exit
	fi

fi
if [ $# -lt 1 ]
then
	read -p "Entrez le nom du fichier qui contient les liens a ouvrir: " fichier

	for i in `cat $fichier`
	do
		brave "'$i'" 
	done
else
	for i in `cat $1`
	do
		brave "$i"
	done
fi
