import os
import sys

# On importe notre nouvelle classe
from image_comparator import ImageComparator

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 test_comparator.py <image_reference.jpg> <image_test.jpg>")
        sys.exit(1)
        
    ref_path = sys.argv[1]
    test_path = sys.argv[2]
    
    print(f"Lancement du test local sur :\n- Réf : {ref_path}\n- Test : {test_path}\n")

    # Initialisation du comparateur (Orienté Objet)
    comparator = ImageComparator(nfeatures=2000, min_match_count=30, distance_threshold=50)

    try:
        # Appel de la méthode compare (avec debug=True pour afficher la fenêtre)
        result = comparator.compare(ref_path, test_path, debug=True)
        
        print("\n--- RÉSULTAT ---")
        if result["match"]:
            print(f"✅ MATCH RÉUSSI ! C'est le même lieu/objet. (Score: {result['score']})")
        else:
            print(f"❌ ÉCHEC. Les images sont différentes ou trop floues. (Score: {result['score']})")
            
        if result["error"]:
            print(f"Détail : {result['error']}")
            
    except Exception as e:
        print(f"Erreur lors de la comparaison : {e}")

if __name__ == "__main__":
    main()
