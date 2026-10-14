import unittest
import numpy as np
import os
from fingerprint import generate_spectrogram, extract_peaks, generate_hashes
from db_sqlite import HashDB

class TestFingerprint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ 
        Génération en mémoire d'un signal et de sa base pour les tests.
        """
        cls.db_path = "test_hashes.db"
        # Nettoyer l'ancienne base de test si elle existe
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
            
        cls.db = HashDB(cls.db_path)

    @classmethod
    def tearDownClass(cls):
        """ Nettoyage de la DB de test """
        cls.db.close()
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_spectrogram_peaks_hashes(self):
        # 1. Générer un signal audio court simulé (ex: 2 secondes de bruit structuré)
        np.random.seed(42)
        y = np.sin(2 * np.pi * 440 * np.linspace(0, 2, 16000 * 2)) + np.random.randn(16000 * 2) * 0.1
        
        # 2. Spectrogramme
        spec = generate_spectrogram(y, sr=16000)
        self.assertTrue(spec.shape[0] > 0 and spec.shape[1] > 0)
        
        # 3. Extraction de pics
        peaks = extract_peaks(spec, amp_min=-60)
        # On s'attend à trouver des pics
        self.assertTrue(len(peaks) > 0)
        
        # 4. Génération des hashes (paires)
        hashes = generate_hashes(peaks)
        self.assertTrue(len(hashes) > 0)
        
        # Le format d'un hash : (string, float_offset)
        self.assertTrue(isinstance(hashes[0][0], str))

    def test_database_insert_match(self):
        # 1. Insertion factice
        fake_hashes = [
            ("hash_A", "khassida_1", "v1", 10.5),
            ("hash_B", "khassida_1", "v1", 12.0),
            ("hash_C", "khassida_2", "v1", 5.0)
        ]
        self.db.insert_hashes(fake_hashes)
        
        # 2. Simulation d'un échantillon utilisateur (match)
        # L'utilisateur envoie l'extrait commençant à 10.0 de la référence k1_v1.
        # Donc sample_offset_A devrait être 0.5 (10.5 - 10.0), B devrait être 2.0 (12.0 - 10.0)
        user_sample = [
            ("hash_A", 0.5),
            ("hash_B", 2.0)
        ]
        
        matches = self.db.find_matches(user_sample)
        
        # On s'attend à trouver une correspondance avec khassida_1, v1
        key = ("khassida_1", "v1")
        self.assertTrue(key in matches)
        
        # Vérification de l'alignement temporel (offset - offset)
        # deltaA = 10.5 - 0.5 = 10.0
        # deltaB = 12.0 - 2.0 = 10.0
        # On voit que l'offset relatif de 10.0 s'aligne ! C'est ce que fera l'orchestrateur.
        self.assertEqual(matches[key], [10.0, 10.0])

if __name__ == '__main__':
    unittest.main()
