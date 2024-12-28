#!/bin/bash
#prend en parametre une commande et verifie s'il est présent dans le répertoire /bin

( cd /bin ; ls $1* &> /dev/null)

if [[ $? == 0 ]]; then
	echo Commande présente code : $?
else 
	echo Commande non présente code : $?
fi