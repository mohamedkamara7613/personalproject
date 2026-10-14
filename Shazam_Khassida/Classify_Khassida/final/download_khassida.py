# -*- coding: utf-8 -*-
import os
import json
import subprocess
import logging
import time
import random
from tqdm import tqdm

# ========= CONFIG =========
AUDIO_DIR = "audios"
DOWNLOADED_IDS_FILE = os.path.join(AUDIO_DIR, "downloaded_ids.json")
PLAYLIST = "https://www.youtube.com/playlist?list=PLJWcF7sUNJKUXQzkI_hRQH9-2KGBtW72A"
MIN_SLEEP = 1
MAX_SLEEP = 1

# ========= LOGGING =========
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# ========= UTILS =========
def load_downloaded_ids():
    if os.path.exists(DOWNLOADED_IDS_FILE):
        with open(DOWNLOADED_IDS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_downloaded_ids(ids_set):
    with open(DOWNLOADED_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(ids_set)), f, indent=2)

# ========= CORE =========
def process_playlist(url: str):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    downloaded_ids = load_downloaded_ids()

    # 1️⃣ Récupération des infos sans télécharger
    cmd_fetch = [
        "yt-dlp",
        "--flat-playlist",
        "--dump-json",
        url
    ]

    try:
        logging.info("🔍 Récupération de la liste des vidéos...")
        result = subprocess.run(cmd_fetch, capture_output=True, text=True, check=True)
        videos = [json.loads(line) for line in result.stdout.splitlines()]
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Erreur lors de la récupération de la playlist : {e}")
        return

    logging.info(f"{len(videos)} vidéos trouvées au total")
    
    # Filter out already downloaded videos
    videos_to_download = [v for v in videos if v["id"] not in downloaded_ids]
    logging.info(f"⏭ {len(videos) - len(videos_to_download)} vidéos déjà téléchargées")
    logging.info(f"📥 {len(videos_to_download)} vidéos restent à télécharger")

    # Progress bar loop
    pbar = tqdm(total=len(videos_to_download), unit="video")

    for video in videos_to_download:
        video_id = video["id"]
        title = video.get("title", "unknown")

        pbar.set_description(f"Téléchargement : {title[:30]}...")
        
        cmd_dl = [
            "yt-dlp",
            f"https://www.youtube.com/watch?v={video_id}",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "192K",
            "--no-playlist", "-v",
            "-o", f"{AUDIO_DIR}/%(title)s.%(ext)s"
        ]

        try:
            subprocess.run(cmd_dl, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            downloaded_ids.add(video_id)
            save_downloaded_ids(downloaded_ids)
            pbar.update(1)
            
            # Pause aléatoire pour éviter le blocage
            wait_time = random.uniform(MIN_SLEEP, MAX_SLEEP)
            time.sleep(wait_time)
            
        except subprocess.CalledProcessError as e:
            logging.error(f"\n❌ Erreur pour {title} : {e}")
        except KeyboardInterrupt:
            logging.info("\n🛑 Interruption par l'utilisateur. Sauvegarde en cours...")
            save_downloaded_ids(downloaded_ids)
            break
            
    pbar.close()
    logging.info("✅ Processus terminé (ou interrompu).")

# ========= MAIN =========
if __name__ == "__main__":
    if PLAYLIST:
        process_playlist(PLAYLIST)
    else:
        playlist_url = input("➡️ URL de la playlist YouTube : ").strip()
        if playlist_url:
            process_playlist(playlist_url)
