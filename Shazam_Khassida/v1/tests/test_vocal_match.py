import unittest
import numpy as np
import os
from vocal_match import extract_mfcc, compute_dtw_distance, VocalDB

class TestVocalMatch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Génère des signaux simulés pour les tests et prépare la base. """
        cls.db_path = "test_chunks_mfcc.pkl"
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)
        cls.db = VocalDB(cls.db_path)
        
        # Signal 1 : Une "voix" simulée (fréquence fondamentale glissante)
        t1 = np.linspace(0, 2, 16000 * 2)
        cls.y1 = np.sin(2 * np.pi * (200 + 50 * t1) * t1)
        
        # Signal 2 : Une légère variation du Signal 1 (même contenu, tempo un peu différent)
        # On le simule en l'étirant légèrement (simple re-échantillonnage de temps)
        t2 = np.linspace(0, 2, 16000 * 2)
        cls.y2 = np.sin(2 * np.pi * (200 + 50 * (t2 * 1.05)) * (t2 * 1.05))
        
        # Signal 3 : Complètement différent (bruit blanc + basse fréquence fixe)
        cls.y3 = np.random.randn(16000 * 2) * 0.1 + np.sin(2 * np.pi * 50 * t1)
        
        # Signal 4 : Exactement y1 mais à moitié volume pour tester la normalisation
        cls.y4 = cls.y1 * 0.5

    @classmethod
    def tearDownClass(cls):
        """ Nettoyage """
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_extract_mfcc(self):
        # Validation du shape et de la normalisation
        mfcc = extract_mfcc(self.y1, sr=16000, n_mfcc=20)
        
        # Le shape attendu dépend du n_fft et hop_length par défaut de librosa
        # mais la dimension 0 doit être n_mfcc (20)
        self.assertEqual(mfcc.shape[0], 20)
        
        # Vérification grossière de la normalisation (mean proche de 0 sur l'axe temporel)
        mean_vals = np.mean(mfcc, axis=1)
        for m in mean_vals:
            self.assertAlmostEqual(m, 0.0, places=5)

    def test_compute_dtw_distance(self):
        mfcc1 = extract_mfcc(self.y1)
        mfcc2 = extract_mfcc(self.y2)
        mfcc3 = extract_mfcc(self.y3)
        mfcc4 = extract_mfcc(self.y4)
        
        # La distance d'un signal à lui-même doit être quasi-nulle
        dist_self = compute_dtw_distance(mfcc1, mfcc1)
        self.assertTrue(dist_self < 1e-5)
        
        # La distance entre y1 et sa version à volume réduit y4 doit aussi être quasi-nulle
        # car les MFCC sont normalisés (robustesse au volume)
        dist_volume = compute_dtw_distance(mfcc1, mfcc4)
        self.assertTrue(dist_volume < 1e-5)
        
        # La distance entre y1 et sa variation y2 doit être mesurable mais "faible"
        dist_similar = compute_dtw_distance(mfcc1, mfcc2)
        
        # La distance avec un signal complètement différent y3 doit être beaucoup plus grande
        dist_different = compute_dtw_distance(mfcc1, mfcc3)
        
        self.assertTrue(dist_similar > 0)
        self.assertTrue(dist_different > dist_similar)
        print(f"\\n[INFO] DTW Identique   : {dist_self:.4f}")
        print(f"[INFO] DTW Vol. Faible : {dist_volume:.4f}")
        print(f"[INFO] DTW Similaire   : {dist_similar:.4f}")
        print(f"[INFO] DTW Différent   : {dist_different:.4f}")

    def test_vocal_db(self):
        # 1. Ajout dans la DB en mémoire
        mfcc_ref = extract_mfcc(self.y1)
        self.db.add_chunk('khassida_1', 'v1', 'chunk_0', mfcc_ref)
        self.db.save_db() # Sauvegarde sur disque
        
        # 2. Re-chargement
        new_db = VocalDB(self.db_path)
        self.assertEqual(len(new_db.chunks_data), 1)
        
        # 3. Test du find_best_match avec une requête similaire (y2)
        query_mfcc = extract_mfcc(self.y2)
        # On met un seuil assez haut (0.50) pour le test car nos signaux sont très simplistes
        best_match, distance = new_db.find_best_match(query_mfcc, threshold=0.50)
        
        self.assertIsNotNone(best_match)
        self.assertEqual(best_match['khassida_id'], 'khassida_1')
        
        # 4. Test avec une requête totalement différente (y3), qui devrait échouer au seuil
        query_mfcc_diff = extract_mfcc(self.y3)
        best_match_fail, distance_fail = new_db.find_best_match(query_mfcc_diff, threshold=0.10)
        self.assertIsNone(best_match_fail)

if __name__ == '__main__':
    unittest.main()
