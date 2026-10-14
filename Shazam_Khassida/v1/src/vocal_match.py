import librosa
import numpy as np
import pickle
import os

def extract_mfcc(y, sr=16000, n_mfcc=20):
    """
    Extrait les coefficients Mel-Frequency Cepstral (MFCC).
    Idéal pour capturer le timbre de la voix a cappella.
    """
    # Calcul des MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    
    # Standardisation sur l'axe du temps (mean 0, var 1)
    # Très important pour rendre le DTW robuste aux variations de volume
    mfcc_norm = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / (np.std(mfcc, axis=1, keepdims=True) + 1e-8)
    
    return mfcc_norm

def compute_dtw_distance(mfcc1, mfcc2):
    """
    Calcule la distance d'alignement temporel dynamique (DTW) entre deux séquences MFCC.
    Plus la distance est faible, plus les extraits sont similaires vocalement.
    """
    # DTW attend des séquences temporelles (Time, Features)
    # Les MFCC de librosa sont (Features, Time), on transpose donc
    D, wp = librosa.sequence.dtw(X=mfcc1, Y=mfcc2, metric='cosine')
    
    # La distance globale est la dernière valeur de la matrice de coût cumulé
    distance = D[-1, -1]
    
    # On normalise la distance par la longueur du chemin d'alignement
    # pour pouvoir comparer des extraits de durées légèrement différentes
    normalized_distance = distance / len(wp)
    
    return normalized_distance

class VocalDB:
    def __init__(self, db_path='data/processed/chunks_mfcc.pkl'):
        self.db_path = db_path
        self.chunks_data = [] # Liste de dicts: {'khassida_id': k, 'version_id': v, 'chunk_id': id, 'mfcc': array}
        self.load_db()
        
    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'rb') as f:
                self.chunks_data = pickle.load(f)
                
    def save_db(self):
        # Assure que le dossier existe
        directory = os.path.dirname(self.db_path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(self.db_path, 'wb') as f:
            pickle.dump(self.chunks_data, f)
            
    def add_chunk(self, khassida_id, version_id, chunk_id, mfcc_matrix):
        """Ajoute un chunk à la base d'empreintes vocales."""
        self.chunks_data.append({
            'khassida_id': khassida_id,
            'version_id': version_id,
            'chunk_id': chunk_id,
            'mfcc': mfcc_matrix
        })
        
    def find_best_match(self, query_mfcc, threshold=0.15):
        """
        Recherche le chunk le plus proche de la requête en parcourant la base (linéaire pour le prototype).
        Retourne (best_match_info, score_distance) ou (None, None) si au-dessus du threshold.
        """
        best_distance = float('inf')
        best_match = None
        
        for item in self.chunks_data:
            dist = compute_dtw_distance(query_mfcc, item['mfcc'])
            if dist < best_distance:
                best_distance = dist
                best_match = item
                
        if best_distance <= threshold:
            return best_match, best_distance
        else:
            return None, best_distance
