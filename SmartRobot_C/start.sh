#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <fichier>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Erreur: fichier '$1' introuvable"
    exit 1
fi

./bin/path_optim "$1" | sudo ./bin/main_elec