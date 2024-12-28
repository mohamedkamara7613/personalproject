#!/bin/bash
read -p "Entrez une suite de mots : " a

set -- $a
echo "Vous avez entré " $# "mots"