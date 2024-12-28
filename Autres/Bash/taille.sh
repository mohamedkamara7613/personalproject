#!/bin/bash
#donne la taille d'un ficher entré en parametre
set -- $(ls -l $1)
echo $5