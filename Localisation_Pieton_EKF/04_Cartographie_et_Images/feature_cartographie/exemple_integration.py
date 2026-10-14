# --- FICHIER D'EXEMPLE POUR LE COLLEGUE ---
# Ce fichier montre comment le collègue devra intégrer ta classe ImageComparator 
# dans son propre fichier resoudre_parcours.py, sans modifier son fichier à sa place.

import sys
import os

# 1. Le collègue devra importer ta classe. 
# S'il place ton fichier image_comparator.py dans le dossier 'core' de son repo, il fera :
# from core.image_comparator import ImageComparator
from image_comparator import ImageComparator # Import local pour cet exemple

def game_loop_du_collegue():
    print("Démarrage du jeu...")
    
    # 2. Le collègue initialise ton comparateur UNE SEULE FOIS au début de son script
    # Il peut ajuster tes paramètres s'il le souhaite (nfeatures, min_match_count...)
    comparateur = ImageComparator()
    
    # ... Le code du collègue tourne (threads, GPS, Kalman, etc.) ...
    
    # ... Le joueur appuie sur le bouton ...
    print("\n[Bouton appuyé] Clic !")
    
    # ... Le collègue fait sa vérification GPS ...
    position_gps_valide = True # (Simulé)
    
    if position_gps_valide:
        print("La position GPS est valide ! Prise de la photo...")
        # ... Le collègue prend la photo avec la caméra et la sauvegarde ...
        photo_prise = "photo_test_camera.jpg"
        photo_reference_a_trouver = "image_cible_du_parcours.jpg"
        
        # 3. Le collègue appelle TA méthode pour vérifier
        print("Appel du module ORB pour vérification...")
        try:
            # result contiendra {"match": True/False, "score": X, "error": Y}
            resultat = comparateur.compare(
                ref_image_input=photo_reference_a_trouver, 
                test_image_input=photo_prise
            )
            
            if resultat["match"]:
                print(f"✅ GAGNÉ ! Le comparateur a trouvé {resultat['score']} points de correspondance.")
                # Le collègue déclenche son buzzer de victoire ici
            else:
                print(f"❌ PERDU ! Ce n'est pas la bonne cible (Score : {resultat['score']}).")
                # Le collègue déclenche son buzzer d'erreur ici
                
        except Exception as e:
            print(f"⚠️ Erreur lors de la comparaison (fichier manquant ?) : {e}")

if __name__ == "__main__":
    game_loop_du_collegue()
