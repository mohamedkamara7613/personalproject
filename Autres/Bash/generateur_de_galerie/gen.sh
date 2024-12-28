#!/bin/bash

#Initialisation des variables par defaut
fichier="galerie"
dossier=""
#Preparation des fichiers et dossiers
if [[ ! -e miniatures ]]
then
	mkdir miniatures
fi

if [ $# -eq 0 ]
then
	rm galerie.html 2>/dev/null
	#Recuperation du nom de dossier des images
	read -p "Entrez le chemin où se trouve les images : " dossier
	if [[ ! -e $dossier ]]; then
		mkdir $dossier
	fi
	#dossier="$dossier/"
	#Entetes du fichier html
	echo "Génération d'En-têtes du fichier html ............................................."
	echo -e "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">" >> $fichier.html
	echo -e "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"fr\" >\n<head>" >> $fichier.html
	echo -e "<title>Ma Galerie</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />" >> $fichier.html
	echo -e "<style type=\"text/css\">a img { border:0; }</style>\n</head>\n<body>\n<p>" >> $fichier.html	
	#Corps du fichier html et inclusion des images
	for image in `ls $dossier*.jpg $dossier*.png $dossier*.jpeg $dossier*.gif 2>/dev/null `
	do
			echo -e "Génération de miniatures de '$image' ..........................................."
			convert $image -thumbnail '200x200>' miniatures/$image
			echo -e "<a href=\"$image\"><img src=\"miniatures/$image\" alt=\"\" /></a>" >> $fichier.html
	done
	#Fin du fichier HTML
	echo -e "</p>\n</body>\n</html>" >> $fichier.html
	echo "Fin de Génération .........................................."
else
	if [ -e $1 ]
	then
		echo -e "Le fichier '$1' existe déjà, Appuyez sur entrer pour le supprimer Ou"
		read -p "tapez q pour quitter : " var
		if [ $var='q' ]; then
			exit
		fi
		mkdir .$1
		mv $1 .$1
		# $1=galerie		
	fi
	#Entetes du fichier html
	echo "Génération d'En-têtes du fichier html ............................................."
	echo -e "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">" >> $1.html
	echo -e "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"fr\" >\n<head>" >> $1.html
	echo -e "<title>Ma Galerie</title>\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />" >> $1.html
	echo -e "<style type=\"text/css\">a img { border:0; }</style>\n</head>\n<body>\n<p>" >> $1.html	
	#Recuperation du nom de dossier des images
	read -p "Entrez le chemin où se trouve les images : " dossier
	if [[ ! -e $dossier ]]; then
		mkdir $dossier
	fi
	#dossier=$dossier/
	#Corps du fichier html et inclusion des images
	for image in `ls $dossier*.jpg $dossier*.png $dossier*.jpeg $dossier*.gif 2>/dev/null`
	do
			echo -e "Génération de miniatures de '$image' ...........................................'"
			convert $image -thumbnail '200x200>' miniatures/$image
			echo -e "<a href=\"$image\"><img src=\"miniatures/$image\" alt=\"\" /></a>" >> $1.html
	done
	#Fin du fichier HTML
	echo -e "</p>\n</body>\n</html>" >> $1.html
	echo "Fin de Génération .........................................."

fi