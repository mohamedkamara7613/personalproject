import unittest
import numpy as np
import os
import soundfile as sf
from db_sqlite import HashDB
from vocal_match import VocalDB
from fingerprint import generate_spectrogram, extract_peaks, generate_hashes
from vocal_match import extract_mfcc
from recognize import KhassidaRecognizer

class TestRecognizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Prépare de faux fichiers audios et de fausses DBs pour simuler le système complet. """
        cls.db_hash_path = "test_orchestrator_hashes.db"
        cls.db_mfcc_path = "test_orchestrator_mfcc.pkl"
        
        # 1. Création d'un "Reference Audio" de 2s et de son "Cover"
        cls.sample_rate = 16000
        t = np.linspace(0, 2, cls.sample_rate * 2)
        # Khassida 1 - Reference
        cls.k1_ref = np.sin(2 * np.pi * 300 * t) + np.sin(2 * np.pi * 600 * t) + np.random.randn(len(t)) * 0.1
        # Khassida 1 - Couverture (tempo très légèrement ralenti, freq modifiée)
        t_slow = np.linspace(0, 2, cls.sample_rate * 2) * 0.95
        cls.k1_cover = np.sin(2 * np.pi * 310 * t_slow) + np.sin(2 * np.pi * 620 * t_slow) + np.random.randn(len(t_slow)) * 0.1
        # Khassida 2 - Reference (Complètement différent)
        cls.k2_ref = np.sin(2 * np.pi * 150 * t) + np.random.randn(len(t)) * 0.1
        
        # Sauvegarde sur disque pour le test d'intégration complet
        cls.file_exact = "test_exact.wav"
        cls.file_cover = "test_cover.wav"
        cls.file_unknown = "test_unknown.wav"
        sf.write(cls.file_exact, cls.k1_ref, cls.sample_rate)
        sf.write(cls.file_cover, cls.k1_cover, cls.sample_rate)
        sf.write(cls.file_unknown, cls.k2_ref, cls.sample_rate)

        # 2. Remplissage des Bases de Données avec "k1_ref"
        # -- Pass 1 (SQLite) --
        if os.path.exists(cls.db_hash_path): os.remove(cls.db_hash_path)
        hash_db = HashDB(cls.db_hash_path)
        spec = generate_spectrogram(cls.k1_ref, sr=cls.sample_rate)
        peaks = extract_peaks(spec)
        hashes = generate_hashes(peaks)
        hash_data = [(h[0], "K1", "V1", h[1]) for h in hashes]
        hash_db.insert_hashes(hash_data)
        hash_db.close()
        
        # -- Pass 2 (Pickle) --
        if os.path.exists(cls.db_mfcc_path): os.remove(cls.db_mfcc_path)
        vocal_db = VocalDB(cls.db_mfcc_path)
        mfcc = extract_mfcc(cls.k1_ref, sr=cls.sample_rate)
        vocal_db.add_chunk("K1", "V1", "C1", mfcc)
        vocal_db.save_db()

    @classmethod
    def tearDownClass(cls):
        """ Nettoyage """
        for f in [cls.db_hash_path, cls.db_mfcc_path, cls.file_exact, cls.file_cover, cls.file_unknown]:
            if os.path.exists(f): os.remove(f)

    def test_pass1_exact_match(self):
        """ Teste si un fichier identique déclenche bien le Pass 1 sans avoir besoin du Pass 2. """
        recognizer = KhassidaRecognizer(self.db_hash_path, self.db_mfcc_path)
        # On abaisse un peu le threshold pour le test car le signal simulé est très court/simple (2s)
        recognizer.threshold_pass1 = 3 
        
        result = recognizer.recognize(self.file_exact)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['method'], 'pass1_fingerprint')
        self.assertEqual(result['match'][0], 'K1')

    def test_pass2_cover_match(self):
        """ Teste si un fichier 'cover' échoue au Pass 1 mais réussit avec le Pass 2 (DTW). """
        recognizer = KhassidaRecognizer(self.db_hash_path, self.db_mfcc_path)
        # On configure pour le signal court de test
        recognizer.threshold_pass1 = 50  # Très haut pour forcer l'échec du pass 1
        recognizer.threshold_pass2 = 0.95 # Assez tolérant pour le signal artificiel bruité
        
        result = recognizer.recognize(self.file_cover)
        
        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['method'], 'pass2_vocal_dtw')
        self.assertEqual(result['match'][0], 'K1')

    def test_unknown_khassida(self):
        """ Teste le rejet total si le son n'est connu ni en Pass 1 ni en Pass 2. """
        recognizer = KhassidaRecognizer(self.db_hash_path, self.db_mfcc_path)
        recognizer.threshold_pass1 = 5
        recognizer.threshold_pass2 = 0.1  # Très strict pour rejeter les faux positifs
        
        result = recognizer.recognize(self.file_unknown)
        
        self.assertEqual(result['status'], 'not_found')
        self.assertEqual(result['method'], 'none')

if __name__ == '__main__':
    unittest.main()
