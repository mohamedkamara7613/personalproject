import numpy as np
import scipy.ndimage as ndimage
import hashlib

def generate_spectrogram(y, sr=16000, n_fft=2048, hop_length=512):
    """
    Génère un spectrogramme (magnitude) à partir d'un signal audio.
    """
    import librosa
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    # On travaille souvent sur le log de la magnitude
    spectrogram = librosa.amplitude_to_db(np.abs(stft), ref=np.max)
    return spectrogram

def extract_peaks(spectrogram, amp_min=-20, neighborhood_size=20):
    """
    Trouve les pics locaux dans le spectrogramme. (CORRIGÉ)
    """
    # Masque booléen des maximums locaux
    local_max = ndimage.maximum_filter(spectrogram, size=neighborhood_size) == spectrogram
    
    # Masque d'amplitude minimale (pour enlever le silence)
    is_loud_enough = spectrogram > amp_min
    
    # On combine : max local ET assez fort
    peaks = local_max & is_loud_enough
    
    # Coordonnées (fréquence_idx, temps_idx) des pics
    freq_bins, time_frames = np.where(peaks)
    
    # Filtrer les très basses fréquences (en dessous de 100Hz = ~13 bins) 
    # pour enlever les bruits de fond/ronflements électriques qui créent des faux positifs
    valid = freq_bins > 15
    freq_bins = freq_bins[valid]
    time_frames = time_frames[valid]
    
    return list(zip(freq_bins, time_frames))

def generate_hashes(peaks, fan_value=15):
    """
    Crée des paires de pics (constellations) et en déduit des hashs.
    peaks : liste de tuples (freq_idx, time_idx) triés par temps.
    fan_value : combien de pics suivants on apparie avec un pic donné.
    Retourne une liste de [(hash_string, time_offset), ...]
    """
    # Tri des pics par ordre temporel
    peaks = sorted(peaks, key=lambda x: x[1])
    
    hashes = []
    for i in range(len(peaks)):
        freq1, t1 = peaks[i]
        count = 0
        for j in range(i + 1, len(peaks)):
            freq2, t2 = peaks[j]
            t_delta = t2 - t1
            
            # On ne veut apparier qu'avec des pics strictement dans le futur
            if t_delta >= 1 and t_delta <= 200:
                hash_str = f"{freq1}|{freq2}|{t_delta}"
                hash_val = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()[:10]
                hashes.append((hash_val, t1))
                count += 1
                
            # On s'arrête si on a trouvé assez de voisins (fan_value) ou si on est trop loin dans le temps
            if count >= fan_value or t_delta > 200:
                break
                
    return hashes
