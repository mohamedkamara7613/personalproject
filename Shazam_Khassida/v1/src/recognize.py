import collections
from preprocess import load_and_clean_audio, separate_hpss
from fingerprint import generate_spectrogram, extract_peaks, generate_hashes
from db_sqlite import HashDB
from vocal_match import extract_mfcc, VocalDB

class KhassidaRecognizer:
    def __init__(self, db_hash_path='data/processed/hashes.db', db_mfcc_path='data/processed/chunks_mfcc.pkl'):
        # Initialisation des deux connexions aux bases de données
        self.hash_db = HashDB(db_path=db_hash_path)
        self.vocal_db = VocalDB(db_path=db_mfcc_path)
        
        # Hyperparamètres
        self.threshold_pass1 = 10 # Nombre minimum d'alignements temporels exacts pour valider le Pass 1
        self.threshold_pass2 = 0.25 # Distance DTW maximale pour valider le Pass 2

    def recognize(self, file_path):
        """
        Orchestrateur Hybride à deux passes.
        Reçoit un extrait audio, tente un match Shazam-like (Pass 1).
        Si échec, tente un match de similarité vocale (Pass 2).
        """
        print(f"\\n🔊 Analyse de l'extrait : {file_path}")
        
        # --- ÉTAPE A : Pré-traitement ---
        # On charge l'audio (mono, 16kHz, normalisé)
        y, sr = load_and_clean_audio(file_path, sr=16000)
        
        # Simuler un enregistrement téléphonique en coupant à 15 secondes max
        max_duration = 15
        if len(y) > max_duration * sr:
            print(f"✂️ Audio trop long. Raccourcissement aux premières {max_duration} secondes...")
            y = y[:max_duration * sr]
        
        
        # --- ÉTAPE B : PASS 1 (Fingerprinting - Shazam) ---
        print("➡️ Lancement du Pass 1 (Fingerprinting - Recherche Exacte)...")
        match_p1, score_p1 = self._run_pass1(y, sr)
        
        if match_p1 and score_p1 >= self.threshold_pass1:
            print(f"✅ SUCCÈS PASS 1 ! Identifié : {match_p1} (Score d'alignement: {score_p1})")
            return {
                'status': 'success',
                'method': 'pass1_fingerprint',
                'match': match_p1,
                'score': score_p1
            }
        
        print(f"❌ Échec Pass 1 (Score max: {score_p1} < {self.threshold_pass1}). L'extrait n'est pas un enregistrement connu exact.")
        
        
        # --- ÉTAPE C : PASS 2 (Similarité Vocale - MFCC + DTW) ---
        print("➡️ Lancement du Pass 2 (Similarité Vocale - Moteur AI Symbolique)...")
        # On nettoie le bruit percussif avec HPSS pour aider le DTW
        y_harmonic = separate_hpss(y)
        
        match_p2, distance_p2 = self._run_pass2(y_harmonic, sr)
        
        if match_p2 and distance_p2 <= self.threshold_pass2:
            print(f"✅ SUCCÈS PASS 2 ! Identifié (Cover/Variation) : {match_p2['khassida_id']} ({match_p2['version_id']}) - Distance DTW: {distance_p2:.4f}")
            return {
                'status': 'success',
                'method': 'pass2_vocal_dtw',
                'match': (match_p2['khassida_id'], match_p2['version_id']),
                'score': distance_p2
            }
            
        print(f"❌ Échec Pass 2 (Meilleure distance: {distance_p2:.4f} > {self.threshold_pass2}).")
        
        # --- ÉTAPE D : Échec Total ---
        print("🤷‍♂️ Khassida non reconnue dans la base actuelle.")
        return {
            'status': 'not_found',
            'method': 'none',
            'match': None,
            'score': None
        }

    def _run_pass1(self, y, sr):
        """ Exécute la logique interne du Pass 1. """
        spec = generate_spectrogram(y, sr=sr)
        peaks = extract_peaks(spec)
        hashes = generate_hashes(peaks)
        
        if not hashes:
            return None, 0
            
        matches = self.hash_db.find_matches(hashes)
        
        # Format matches: { ('khassida_1', 'v1'): [10.5, 10.5, 10.5, 15.2, ...] }
        best_match = None
        highest_alignment_score = 0
        
        for k_v_tuple, offsets in matches.items():
            # Compter l'offset le plus fréquent (C'est la magie de Shazam !)
            # Pour éviter les problèmes d'arrondis des floats, on arrondit à 1 décimale
            rounded_offsets = [round(o, 1) for o in offsets]
            counter = collections.Counter(rounded_offsets)
            
            if counter:
                top_offset, count = counter.most_common(1)[0]
                if count > highest_alignment_score:
                    highest_alignment_score = count
                    best_match = k_v_tuple
                    
        return best_match, highest_alignment_score

    def _run_pass2(self, y_harmonic, sr):
        """ Exécute la logique interne du Pass 2. """
        query_mfcc = extract_mfcc(y_harmonic, sr=sr)
        best_match, distance = self.vocal_db.find_best_match(query_mfcc, threshold=self.threshold_pass2)
        return best_match, distance
