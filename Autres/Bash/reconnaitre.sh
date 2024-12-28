#!/bin/bash
#		@(#)reconnaitre

shopt -s extglob 
read -p "Entrez un mot : " $mot

case $mot in
	+([[:digit:]]) ) echo "ce mot commence par un nombre";;
	+([[:upper:]]) ) echo "ce mot commence par une lettre magiscule";;
	+([[:lower:]]) ) echo "ce mot commence par une lettre minuscule";;
	*) echo "Commence par une autre sorte de caractere"
esac
	

