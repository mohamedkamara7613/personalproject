#!/usr/bin/env python3
import cv2
import sys
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 compare_two_images.py <image_reference.jpg> <image_test.jpg>")
        sys.exit(1)
        
    ref_path = sys.argv[1]
    test_path = sys.argv[2]
    
    for path in [ref_path, test_path]:
        if not os.path.exists(path):
            print(f"Erreur : Le fichier '{path}' n'existe pas.")
            sys.exit(1)

    print(f"Comparaison de : [{ref_path}]  vs  [{test_path}]")

    # 1. Chargement en niveau de gris
    img1 = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(test_path, cv2.IMREAD_GRAYSCALE)

    # Réduire la taille des images si elles viennent d'un smartphone (souvent énormes type 4000x3000)
    # On les redimensionne à une largeur max de 800px pour que l'algorithme soit rapide et affiche bien
    def resize_img(img, max_width=800):
        h, w = img.shape
        if w > max_width:
            ratio = max_width / w
            return cv2.resize(img, (max_width, int(h * ratio)))
        return img
        
    img1 = resize_img(img1)
    img2 = resize_img(img2)

    # 2. Initialisation d'ORB
    orb = cv2.ORB_create(nfeatures=2000) # Plus de features car les photos de tel sont grandes
    
    # 3. Calcul des points clés (Keypoints) et Descripteurs
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    
    print(f"Points détectés -> Réf : {len(kp1)} | Test : {len(kp2)}")

    if des1 is None or des2 is None:
        print("Erreur : Impossible de trouver des points caractéristiques sur l'une des images.")
        sys.exit(1)

    # 4. Matching (Brute-Force Matcher)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    
    # 5. Tri par distance (les plus petits sont les meilleurs)
    matches = sorted(matches, key=lambda x: x.distance)
    
    # 6. Filtrer les "Bons" matchs (Distance < 50 est une bonne règle de base pour ORB)
    good_matches = [m for m in matches if m.distance < 50]
    
    match_count = len(good_matches)
    print(f"Nombre de correspondances valides trouvées : {match_count}")
    
    MIN_MATCH_COUNT = 30 # Seuil pour considérer que c'est le même lieu
    
    if match_count >= MIN_MATCH_COUNT:
        print("✅ RÉSULTAT : MATCH RÉUSSI ! C'est le même lieu/objet.")
    else:
        print("❌ RÉSULTAT : ÉCHEC. Les images sont trop différentes.")

    # 7. Affichage visuel (relie les points d'une image à l'autre)
    # On dessine les 50 meilleurs matchs pour ne pas surcharger l'écran
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches[:50], None, 
                                  flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                                  matchColor=(0, 255, 0))
    
    cv2.imshow("Resultat ORB (Espace pour quitter)", img_matches)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
