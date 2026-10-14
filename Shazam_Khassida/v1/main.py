import sys
import os
import argparse
sys.path.insert(0, os.path.abspath('src'))
from recognize import KhassidaRecognizer
from build_db import build_database

def main():
    parser = argparse.ArgumentParser(description="Shazam Khassida - Système de Reconnaissance Hybride")
    subparsers = parser.add_subparsers(dest="command", help="Commandes disponibles")

    # Commande 1 : build
    parser_build = subparsers.add_parser("build", help="Construit ou met à jour les bases de données depuis data/ref/")
    
    # Commande 2 : recognize
    parser_recognize = subparsers.add_parser("recognize", help="Tente de reconnaitre un fichier audio")
    parser_recognize.add_argument("file", type=str, help="Chemin vers le fichier audio (.wav) à analyser")

    args = parser.parse_args()

    if args.command == "build":
        build_database()
    
    elif args.command == "recognize":
        if not os.path.exists(args.file):
            print(f"❌ Erreur : Le fichier {args.file} est introuvable.")
            sys.exit(1)
            
        print(f"🎵 Lancement de l'Orchestrateur Shazam Khassida sur {args.file}")
        
        # On instancie l'orchestrateur avec nos seuils de production
        recognizer = KhassidaRecognizer()
        
        # En production, les seuils sont plus stricts pour éviter les faux positifs (bruits de fond)
        recognizer.threshold_pass1 = 15   # Au moins 15 points d'ancrage temporels
        recognizer.threshold_pass2 = 0.25 # Tolérance DTW très stricte (0.25)
        
        result = recognizer.recognize(args.file)
        
        if result['status'] == 'success':
            khassida_id, version_id = result['match']
            print("\n" + "="*50)
            print(f"🎙️ MASHALLAH KHASSIDA RECONNU ! 🎙️")
            print(f"➤ Khassida : {khassida_id}")
            print(f"➤ Version originale : {version_id}")
            print(f"➤ Méthode de reconnaissance : {result['method']}")
            print(f"➤ Score de confiance : {result['score']:.4f}")
            print("="*50 + "\n")
        else:
            print("\n" + "="*50)
            print("😔 KHASSIDA NON RECONNU")
            print("➤ L'extrait n'est ni un original, ni une cover connue de la base de données.")
            print("="*50 + "\n")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
