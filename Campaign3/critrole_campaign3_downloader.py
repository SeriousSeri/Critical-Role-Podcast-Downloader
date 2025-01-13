#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
import feedparser

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

FEED_URL = "https://feeds.simplecast.com/LXz4Q9rJ"
DOWNLOAD_FOLDER = "campaign3_bellshells"  # Using the established folder name

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

# Regex to match Campaign 3 episode patterns like "C3E<number>" or "C3 E<number>"
campaign3_regex = re.compile(r"C3\s*E\d+", re.IGNORECASE)

def sanitize_filename(name: str) -> str:
    """
    Sanitize the filename by normalizing "C3 E<number>" to "C3E<number>",
    removing unwanted characters, and replacing spaces with underscores.
    """
    name = re.sub(r"(C3)\s*E(\d+)", r"\1E\2", name, flags=re.IGNORECASE)
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def add_id3_tags(filepath: str, title: str):
    """
    Add ID3 tags to the downloaded MP3 file, ensuring the title tag follows the
    consistent naming scheme (e.g., "C3E123").
    """
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath)
    
    # Normalize the title to a consistent "C3E<number>" format
    normalized_title = re.sub(r"(C3)\s*E(\d+)", r"\1E\2", title, flags=re.IGNORECASE)
    
    audio["title"] = normalized_title
    audio["artist"] = "Critical Role"
    audio["album"] = "Campaign 3: Bells Hells"
    audio.save()

def main():
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    print(f"Fetching feed from: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    episodes = feed.entries
    print(f"Found {len(episodes)} episodes in the feed.\n")

    # Load already downloaded episode titles to avoid duplicates
    downloaded_db_file = "downloaded_campaign3.txt"
    downloaded = set()
    if os.path.exists(downloaded_db_file):
        with open(downloaded_db_file, "r", encoding="utf-8") as f:
            for line in f:
                downloaded.add(line.strip())

    downloaded_count = 0
    idx = 1

    for entry in episodes:
        title = entry.title

        # Filter for standard Campaign 3 episodes
        # Skip if title does not match Campaign 3 pattern or contains unwanted substrings
        if not (campaign3_regex.search(title) or ("Campaign 3" in title)) \
           or ("4-Sided Dive" in title) or ("FEED DROP" in title):
            print(f"[{idx}] Skipping non-standard Campaign 3 episode: '{title}'")
            idx += 1
            continue

        # Skip if already downloaded
        if title in downloaded:
            print(f"[{idx}] Already downloaded: '{title}'")
            idx += 1
            continue

        enclosures = entry.get("enclosures", [])
        if not enclosures:
            print(f"[{idx}] No enclosure found for '{title}', skipping.")
            idx += 1
            continue

        mp3_url = enclosures[0].get("href")
        if not mp3_url:
            print(f"[{idx}] No MP3 URL found for '{title}', skipping.")
            idx += 1
            continue

        filename = sanitize_filename(title) + ".mp3"
        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        if os.path.exists(file_path):
            print(f"[{idx}] Already exists: {filename} - Skipping.")
            downloaded.add(title)
            idx += 1
            continue

        print(f"[{idx}] Downloading: {title} => {filename}")
        try:
            with requests.get(mp3_url, headers=HEADERS, stream=True) as resp:
                resp.raise_for_status()
                with open(file_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            add_id3_tags(file_path, title)
            downloaded_count += 1
            print(f"   -> Finished: {file_path}")

            downloaded.add(title)
            with open(downloaded_db_file, "a", encoding="utf-8") as db:
                db.write(title + "\n")
        except Exception as e:
            print(f"   -> Error downloading '{title}': {e}")

        idx += 1

    print(f"\nAll episodes processed. Total downloaded: {downloaded_count}")

if __name__ == "__main__":
    main()
