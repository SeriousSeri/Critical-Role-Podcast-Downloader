#!/usr/bin/env python3
import feedparser
import os
import requests
import re

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

# URL of the Simplecast feed
FEED_URL = "https://feeds.simplecast.com/LXz4Q9rJ"

# Base folder where episodes will be saved
DOWNLOAD_FOLDER = "special_episodes"

# Compile a regex to identify any campaign episode codes like "C<number>E<number>"
campaign_regex = re.compile(r"C\d+\s*E\d+", re.IGNORECASE)

def sanitize_filename(name: str) -> str:
    """
    Sanitize the filename by standardizing campaign codes (e.g., "C3 E123" to "C3E123"),
    removing unwanted characters, and replacing spaces with underscores.
    """
    name = re.sub(r"(C\d+)\s*E(\d+)", r"\1E\2", name, flags=re.IGNORECASE)
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def add_id3_tags(filepath: str, title: str, album: str):
    """
    Add ID3 tags to the downloaded MP3 file, setting title, artist, and album.
    """
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
    audio["title"] = title
    audio["artist"] = "Critical Role"
    audio["album"] = album
    audio.save(filepath)

def main():
    print(f"Fetching feed from: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    total = len(feed.entries)
    print(f"Found {total} episodes in the feed.")

    downloaded_db_file = "downloaded_specials.txt"
    downloaded = set()
    if os.path.exists(downloaded_db_file):
        with open(downloaded_db_file, "r", encoding="utf-8") as f:
            for line in f:
                downloaded.add(line.strip())

    idx = 1
    for entry in feed.entries:
        title = entry.title

        # Skip standard campaign episodes unless part of "4-Sided Dive"
        # Also skip the "Welcome to Beacon" ad episode
        if ("Welcome to Beacon" in title) or (campaign_regex.search(title) and "4-Sided Dive" not in title):
            print(f"[{idx}] Skipping campaign/ad episode: '{title}'")
            idx += 1
            continue

        if title in downloaded:
            print(f"[{idx}] Already downloaded: '{title}'")
            idx += 1
            continue

        # Determine destination folder based on title keywords
        folder = "Misc"
        if "One-Shot" in title:
            folder = "One-Shot"
        elif "4-Sided Dive" in title:
            folder = "4-Sided Dive"
        elif "Exandria Unlimited" in title:
            folder = "Exandria Unlimited"

        folder_path = os.path.join(DOWNLOAD_FOLDER, folder)
        os.makedirs(folder_path, exist_ok=True)

        if 'enclosures' in entry and len(entry.enclosures) > 0:
            mp3_url = entry.enclosures[0].href
            filename = sanitize_filename(title) + ".mp3"
            file_path = os.path.join(folder_path, filename)

            print(f"[{idx}] Downloading: {title} into folder '{folder}' as {filename}")
            try:
                response = requests.get(mp3_url, stream=True)
                response.raise_for_status()

                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"   -> Finished: {file_path}")

                # Add ID3 tags with album set to folder name
                add_id3_tags(file_path, title, folder)

                downloaded.add(title)
                with open(downloaded_db_file, "a", encoding="utf-8") as db:
                    db.write(title + "\n")
            except Exception as e:
                print(f"Error downloading {title}: {e}")
        else:
            print(f"[{idx}] No enclosure found for item: '{title}', skipping.")

        idx += 1

    print("All done.")

if __name__ == "__main__":
    main()
