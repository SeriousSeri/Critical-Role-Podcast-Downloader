#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import feedparser
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

FEED_URL = "https://feeds.simplecast.com/LXz4Q9rJ"
DOWNLOAD_FOLDER = "campaign2_mightynein"  # Korrigierter Ordnername

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def sanitize_filename(name: str) -> str:
    import re
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def add_id3_tags(filepath: str, title: str):
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath)
    audio["title"] = title
    audio["artist"] = "Critical Role"
    audio["album"] = "Campaign 2: The Mighty Nein"
    audio.save()

def main():
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    print(f"Fetching feed from: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    episodes = feed.entries
    print(f"Found {len(episodes)} episodes in the feed.\n")

    downloaded = 0
    for idx, entry in enumerate(episodes, start=1):
        title = entry.title

        # Filter: Nur Episoden von Campaign 2 basierend auf dem Titel verarbeiten
        if not (("C2E" in title) or ("Campaign 2" in title)):
            print(f"[{idx}] Skipping non-Campaign2 episode: '{title}'")
            continue

        enclosures = entry.get("enclosures", [])
        if not enclosures:
            print(f"[{idx}] No enclosure found for '{title}', skipping.")
            continue

        mp3_url = enclosures[0].get("href")
        if not mp3_url:
            print(f"[{idx}] No MP3 URL found for '{title}', skipping.")
            continue

        # Dateinamen ohne doppelten Präfix erzeugen
        filename = sanitize_filename(title) + ".mp3"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        if os.path.exists(filepath):
            print(f"[{idx}] Already exists: {filename} - Skipping.")
            continue

        print(f"[{idx}] Downloading: {title} => {filename}")
        try:
            with requests.get(mp3_url, headers=HEADERS, stream=True) as resp:
                resp.raise_for_status()
                with open(filepath, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            add_id3_tags(filepath, title)
            downloaded += 1
            print(f"   -> Finished: {filepath}")
        except Exception as e:
            print(f"   -> Error downloading '{title}': {e}")

    print(f"\nAll episodes processed. Total downloaded: {downloaded}")

if __name__ == "__main__":
    main()
