import unittest
import numpy as np
import os
import soundfile as sf
from preprocess import load_and_clean_audio, separate_hpss, chunk_audio, process_pipeline

class TestPreprocess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Création d'un fichier audio factice pour les tests (Bruit blanc + Sinusoïde)
        """
        cls.test_file = "dummy_test_audio.wav"
        cls.test_sr = 22050
        # Audio de 30 secondes
        t = np.linspace(0, 30, 30 * cls.test_sr, endpoint=False)
        # Signal mixte : note de 440Hz + bruit blanc
        audio_data = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.random.randn(len(t))
        sf.write(cls.test_file, audio_data, cls.test_sr)

    @classmethod
    def tearDownClass(cls):
        """ Nettoyage du fichier factice """
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    def test_load_and_clean_audio(self):
        y, sr = load_and_clean_audio(self.test_file, sr=16000)
        self.assertEqual(sr, 16000)
        # La durée doit être préservée (30 secondes)
        self.assertEqual(len(y), 16000 * 30)
        # Le volume doit être normalisé (max peak = 1.0)
        self.assertAlmostEqual(np.max(np.abs(y)), 1.0, places=2)

    def test_separate_hpss(self):
        # Tester de la séparation avec un signal généré en mémoire
        y = np.random.randn(16000 * 2) # 2 secondes de bruit
        y_harmonic = separate_hpss(y)
        self.assertEqual(len(y_harmonic), len(y))
        # Vérifier qu'on obtient bien un tableau numpy
        self.assertTrue(isinstance(y_harmonic, np.ndarray))

    def test_chunk_audio(self):
        # Signal factice de 35 secondes en mémoire
        y = np.ones(16000 * 35) 
        chunks = chunk_audio(y, sr=16000, chunk_duration=15, overlap=5)
        
        # Répartition attendue (pas de 10s grâce à l'overlap de 5s pour des chunks de 15s) :
        # chunk 0: 0s à 15s  (start: 0)
        # chunk 1: 10s à 25s (start: 10)
        # chunk 2: 20s à 35s (start: 20)
        # chunk 3: 30s à 35s (start: 30) - chunk tronqué final de 5s
        
        self.assertEqual(len(chunks), 4)
        
        # Test des temps de début
        self.assertEqual(chunks[0]['start_time'], 0.0)
        self.assertEqual(chunks[1]['start_time'], 10.0)
        self.assertEqual(chunks[2]['start_time'], 20.0)
        self.assertEqual(chunks[3]['start_time'], 30.0)
        
        # Test des durées
        self.assertEqual(chunks[0]['duration'], 15.0)
        self.assertEqual(chunks[3]['duration'], 5.0)

    def test_process_pipeline(self):
        chunks = process_pipeline(self.test_file, sr=16000, chunk_duration=15, overlap=5, apply_hpss=True)
        self.assertTrue(len(chunks) > 0)
        self.assertEqual(chunks[0]['duration'], 15.0)

if __name__ == '__main__':
    unittest.main()
