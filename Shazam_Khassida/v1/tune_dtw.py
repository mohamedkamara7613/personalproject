import os
import glob
import numpy as np
from src.preprocess import load_and_clean_audio, separate_hpss
from src.vocal_match import extract_mfcc, VocalDB

def evaluate_dtw(vocal_db_path='data/processed/chunks_mfcc.pkl', target_khassida='midadi', pos_dir='data/eval/positives', neg_dir='data/eval/negatives'):
    """
    Évalue les performances du Pass 2 (DTW) sur un jeu de données annoté.
    - pos_dir : extraits audio qui SONT le target_khassida (Vrais Positifs)
    - neg_dir : extraits audio qui NE SONT PAS le target_khassida (Vrais Négatifs)
    """
    print(f"🚀 Début de l'évaluation du seuil DTW pour la cible : {target_khassida}\n")
    
    if not os.path.exists(vocal_db_path):
        print(f"❌ Erreur : Base {vocal_db_path} introuvable. Lancez 'python main.py build' d'abord.")
        return
        
    vocal_db = VocalDB(db_path=vocal_db_path)
    
    # 1. Évaluer les Positifs
    print("--- 🟢 ÉVALUATION DES VRAIS POSITIFS (Devrait matcher) ---")
    pos_scores = []
    if os.path.exists(pos_dir):
        files = glob.glob(os.path.join(pos_dir, "*.*"))
        for f in files:
            if not f.endswith(('.wav', '.mp3', '.m4a', '.ogg')): continue
            score = _process_file(f, vocal_db, target_khassida)
            if score is not None:
                pos_scores.append(score)
            print(f"[{os.path.basename(f)}] => Distance DTW vers {target_khassida} : {score:.4f}" if score else f"[{os.path.basename(f)}] => Échec lecture")
    else:
        print(f"Dossier {pos_dir} introuvable.")
        
    # 2. Évaluer les Négatifs
    print("\n--- 🔴 ÉVALUATION DES VRAIS NÉGATIFS (Ne devrait PAS matcher) ---")
    neg_scores = []
    if os.path.exists(neg_dir):
        files = glob.glob(os.path.join(neg_dir, "*.*"))
        for f in files:
            if not f.endswith(('.wav', '.mp3', '.m4a', '.ogg')): continue
            score = _process_file(f, vocal_db, target_khassida)
            if score is not None:
                neg_scores.append(score)
            print(f"[{os.path.basename(f)}] => Distance DTW vers {target_khassida} : {score:.4f}" if score else f"[{os.path.basename(f)}] => Échec lecture")
    else:
        print(f"Dossier {neg_dir} introuvable.")
        
    # 3. Bilan chiffré
    print("\n" + "="*50)
    print("📊 BILAN STATISTIQUE DES DISTANCES DTW")
    print("="*50)
    if pos_scores:
        print(f"🟢 POSITIFS : Min={np.min(pos_scores):.4f} | Max={np.max(pos_scores):.4f} | Moyenne={np.mean(pos_scores):.4f}")
    if neg_scores:
        print(f"🔴 NÉGATIFS : Min={np.min(neg_scores):.4f} | Max={np.max(neg_scores):.4f} | Moyenne={np.mean(neg_scores):.4f}")
        
    if pos_scores and neg_scores:
        max_pos = np.max(pos_scores)
        min_neg = np.min(neg_scores)
        print("\nRecommandation de Seuil (Threshold Pass 2) :")
        if max_pos < min_neg:
            print(f"✅ SÉPARATION PARFAITE ! Le seuil idéal se situe entre {max_pos:.4f} et {min_neg:.4f}.")
            print(f"👉 Suggesion: threshold_pass2 = {(max_pos + min_neg) / 2 :.4f}")
        else:
            print("⚠️ CHEVAUCHEMENT (OVERLAP) DÉTECTÉ.")
            print(f"Certains positifs {max_pos:.4f} sont plus éloignés que certains négatifs {min_neg:.4f}.")
            print("Il faudra choisir un compromis (accepter des Faux Positifs ou des Faux Négatifs).")

def _process_file(filepath, vocal_db, target_khassida):
    """Extrait MFCC 15s, et trouve la meilleure distance dans la DB par rapport à target_khassida."""
    try:
        y, sr = load_and_clean_audio(filepath, sr=16000)
        # Tronquer à 15s si trop long
        max_duration = 15
        if len(y) > max_duration * sr:
            y = y[:max_duration * sr]
            
        y_harmonic = separate_hpss(y)
        query_mfcc = extract_mfcc(y_harmonic, sr=sr)
        
        # On ne veut tester la distance QUE sur le khassida cible pour voir si ça matche
        # On va créer un sous-dictionnaire temporaire avec juste la cible
        target_dict = {
            (kid, vid, cid): data 
            for (kid, vid, cid), data in vocal_db.db.items() 
            if kid == target_khassida
        }
        
        if not target_dict:
            print(f"Aucune référence trouvée pour {target_khassida} dans la base.")
            return None
            
        # Appel direct à librosa DTW car find_best_match cherche sur toute la base
        import librosa
        best_dist = float('inf')
        
        for key, data in target_dict.items():
            db_mfcc = data['mfcc']
            D, wp = librosa.sequence.dtw(X=query_mfcc, Y=db_mfcc, metric='cosine')
            dist = D[-1, -1] / len(wp)
            if dist < best_dist:
                best_dist = float(dist)
                
        return best_dist
    except Exception as e:
        print(f"  Erreur sur {filepath}: {e}")
        return None

if __name__ == "__main__":
    # S'assurer que les dossiers de test existent
    os.makedirs('data/eval/positives', exist_ok=True)
    os.makedirs('data/eval/negatives', exist_ok=True)
    
    evaluate_dtw()
