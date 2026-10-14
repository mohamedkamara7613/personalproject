import librosa
import numpy as np

def load_and_clean_audio(file_path, sr=16000):
    """
    Charge l'audio, convertit en mono, resample à `sr` Hz, et normalise le volume.
    """
    # librosa.load convertit nativement en mono et resample si 'sr' est spécifié
    y, _ = librosa.load(file_path, sr=sr, mono=True)
    
    # Normalisation du volume (peak à 1.0)
    max_amp = np.max(np.abs(y))
    if max_amp > 0:
        y = y / max_amp
        
    return y, sr

def separate_hpss(y):
    """
    Applique la séparation Harmonique/Percussive (HPSS) pour isoler la voix.
    Retourne la composante harmonique.
    """
    y_harmonic, _ = librosa.effects.hpss(y)
    return y_harmonic

def chunk_audio(y, sr=16000, chunk_duration=15, overlap=5):
    """
    Découpe l'audio en segments de `chunk_duration` secondes, 
    avec un chevauchement (`overlap`) en secondes.
    Retourne une liste de dictionnaires contenant le segment audio et son temps de début.
    """
    chunk_samples = chunk_duration * sr
    step_samples = (chunk_duration - overlap) * sr
    
    chunks = []
    total_samples = len(y)
    
    for start_idx in range(0, total_samples, step_samples):
        end_idx = start_idx + chunk_samples
        chunk = y[start_idx:end_idx]
        
        # Ignorer les chunks de moins d'1 seconde (trop courts pour être pertinents)
        if len(chunk) < sr * 1: 
            break
            
        chunks.append({
            'audio': chunk,
            'start_time': start_idx / sr,
            'duration': len(chunk) / sr
        })
        
    return chunks

def process_pipeline(file_path, sr=16000, chunk_duration=15, overlap=5, apply_hpss=True):
    """
    Pipeline complet de pré-traitement pour le MODULE 1.
    Charge, nettoie, applique HPSS (optionnel) et découpe en chunks.
    """
    y, _ = load_and_clean_audio(file_path, sr=sr)
    
    if apply_hpss:
        y = separate_hpss(y)
        
    chunks = chunk_audio(y, sr=sr, chunk_duration=chunk_duration, overlap=overlap)
    return chunks
