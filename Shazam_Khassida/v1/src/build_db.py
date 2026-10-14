import os
import glob
from preprocess import load_and_clean_audio, separate_hpss, chunk_audio
from fingerprint import generate_spectrogram, extract_peaks, generate_hashes
from db_sqlite import HashDB
from vocal_match import extract_mfcc, VocalDB

def build_database(raw_data_dir="data/ref", db_hash_path="data/processed/hashes.db", db_mfcc_path="data/processed/chunks_mfcc.pkl"):
    """
    Parcourt le dossier data/raw/, traite tous les fichiers audio .wav,
    et les insère dans les bases de données Pass 1 (SQLite) et Pass 2 (Pickle).
    
    Structure attendue:
    data/ref/
      └── Khassida_A/
          ├── Version_Originale.wav
          └── Cover_Studio.wav
      └── Khassida_B/
          └── Chant_Accapela.wav
    """
    if not os.path.exists(raw_data_dir):
        print(f"Le dossier {raw_data_dir} n'existe pas. Création...")
        os.makedirs(raw_data_dir, exist_ok=True)
        print("Veuillez y placer vos dossiers de Khassidas et relancer le script.")
        return

    # Suppression des anciennes bases pour repartir à zéro
    if os.path.exists(db_hash_path):
        os.remove(db_hash_path)
    if os.path.exists(db_mfcc_path):
        os.remove(db_mfcc_path)

    # Connexion aux bases de données
    os.makedirs(os.path.dirname(db_hash_path), exist_ok=True)
    hash_db = HashDB(db_path=db_hash_path)
    vocal_db = VocalDB(db_path=db_mfcc_path)
    
    # Parcourir chaque dossier (Khassida_ID)
    khassida_dirs = [d for d in os.listdir(raw_data_dir) if os.path.isdir(os.path.join(raw_data_dir, d))]
    
    # Extensions supportées pour la conversion automatique
    supported_extensions = ('.wav', '.mp3', '.m4a', '.ogg', '.flac')
    
    total_files = 0
    for khassida_id in khassida_dirs:
        khassida_path = os.path.join(raw_data_dir, khassida_id)
        
        # Trouver tous les fichiers audio supportés
        audio_files = []
        for ext in supported_extensions:
            audio_files.extend(glob.glob(os.path.join(khassida_path, f"*{ext}")))
            audio_files.extend(glob.glob(os.path.join(khassida_path, f"*{ext.upper()}")))
        
        for audio_file in set(audio_files): # set() pour éviter les doublons au cas où
            version_id = os.path.splitext(os.path.basename(audio_file))[0]
            ext = os.path.splitext(audio_file)[1].lower()
            print(f"\n⚙️ Traitement de: {khassida_id} -> {version_id} ({ext})")
            
            try:
                # Librosa peut lire nativement la plupart des formats, donc pas de conversion préalable nécessaire.
                # On s'assure juste que l'extension est supportée par librosa (ou au moins les plus courantes)
                if ext not in ['.wav', '.mp3', '.m4a', '.ogg', '.flac']:
                    print(f"   ⚠️ Format non supporté par librosa pour l'indexation : {ext}. Fichier ignoré.")
                    continue
                    
                # 1. Chargement et Nettoyage
                y, sr = load_and_clean_audio(audio_file)
                y_harmonic = separate_hpss(y)
                
                # 2. Chunking (Segments de 15s avec 5s de chevauchement)
                # On chunk l'audio complet (pour le Shazam-like)
                chunks_mixed = chunk_audio(y, sr, chunk_duration=15, overlap=5)
                # On chunk l'audio vocal (pour le MFCC + DTW)
                chunks_harmonic = chunk_audio(y_harmonic, sr, chunk_duration=15, overlap=5)

                for i, chunk_dict in enumerate(chunks_mixed):
                    chunk_id = f"chunk_{i:03d}"
                    chunk_y = chunk_dict['audio']
                    
                    # --- PASS 1: Fingerprinting (sur le mix complet) ---
                    spec = generate_spectrogram(chunk_y, sr)
                    peaks = extract_peaks(spec)
                    hashes = generate_hashes(peaks)
                    
                    if hashes:
                        # Calcul de l'offset absolu : l'index frame = (temps de début) * sr / hop_length
                        # librosa génère un frame tous les hop_length (512 par défaut dans fingerprint.py)
                        hop_length = 512
                        chunk_start_frame = int(chunk_dict['start_time'] * sr / hop_length)
                        
                        # Format attendu par HashDB: (hash, khassida_id, version_id, absolute_offset)
                        hash_data = [(h[0], khassida_id, version_id, float(h[1] + chunk_start_frame)) for h in hashes]
                        hash_db.insert_hashes(hash_data)
                    
                    # --- PASS 2: MFCC (sur la partie vocale "harmonic") ---
                    chunk_y_harm = chunks_harmonic[i]['audio'] # On récupère le bout harmonique correspondant
                    mfcc = extract_mfcc(chunk_y_harm, sr)
                    vocal_db.add_chunk(khassida_id, version_id, chunk_id, mfcc)
                
                print(f"✅ Terminé : {len(chunks_mixed)} chunks extraits et indexés.")
                total_files += 1

            except Exception as e:
                print(f"❌ Erreur lors du traitement de {audio_file} : {e}")

    # Nettoyage et Sauvegarde Finale
    hash_db.close()
    vocal_db.save_db()
    print(f"\\n🎉 Indexation terminée ! {total_files} fichiers indexés avec succès.")

if __name__ == "__main__":
    print("🚀 Lancement du constructeur de Base de Données Shazam Khassida...")
    build_database()
