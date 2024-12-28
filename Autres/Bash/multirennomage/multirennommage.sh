#!/bin/bash

while [ $# -lt 1 ] #Si aucun parametre n'est envoyé on demande a l'utilisateur de tapez le nom des fichiers a rennomé
do
	read -p "Entrez le nom du fichier a rennomé (ou tapez q pour quitter) : " fichier
	echo "Rennomage de '$fichier' .................."
	if [[ $fichier = 'q' ]]; then
		exit
	fi
	mv $fichier $fichier-old
done

if [ $# -le 9 ] #S'il y a moins de 9 parametres, on les renommes tous
then
	for i in $1 $2 $3 $4 $5 $6 $7 $8 $9
	do
		echo -e "Rennomage de '$i' ................"
		mv $i $i-old
	done
else #S'il y en a plus on decale le neuvieme de 1 param a chaque passage de boucle et on le renomme
	for i in $1 $2 $3 $4 $5 $6 $7 $8 $9
	do
		echo -e "Rennomage de '$i' ................"
		mv $i $i-old
	done
	let "paramSuplement=$# - 9"
	for i in `seq 1 $paramSuplement`
	do
		shift
		echo -e "Rennomage de '$9' ................"
		mv $9 $9-old
	done
fi
