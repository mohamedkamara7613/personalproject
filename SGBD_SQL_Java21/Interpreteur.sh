#!/bin/bash

# 1. Compilation du projet
echo "========================================"
echo "    Compilation du projet en cours...   "
echo "========================================"
make comp

# Vérification si la compilation a réussi
if [ $? -ne 0 ]; then
    echo "[ERREUR] La compilation a échoué. Arrêt du script."
    exit 1
fi


echo ""
echo "========================================"
echo "    Démarrage du Mini-SGBD INSA         "
echo "========================================"
echo "Comment veux-tu lancer l'interpréteur ?"
echo "1 - Mode Console (Interactif)"
echo "2 - Exécuter un fichier SQL"
echo "========================================"
read -p "Ton choix (1 ou 2) : " choix

# 3. Lancement selon le choix
if [ "$choix" = "1" ]; then
    echo -e "\nLancement du mode console..."
    java -cp ./classes fr.insarouen.iti.prog.sgbd.execution.Interpreteur

elif [ "$choix" = "2" ]; then
    read -p "Entrez le chemin du fichier SQL (ex: Exemples/test_jointure.sql) : " fichier
    
    # Vérifie que le fichier existe bien avant de lancer Java
    if [ -f "$fichier" ]; then
        echo -e "\nExécution du fichier : $fichier..."
        java -cp ./classes fr.insarouen.iti.prog.sgbd.execution.Interpreteur "$fichier"
    else
        echo "[ERREUR] Le fichier '$fichier' est introuvable."
        exit 1
    fi

else
    echo "[ERREUR] Choix invalide. Veuillez relancer le script et taper 1 ou 2."
    exit 1
fi