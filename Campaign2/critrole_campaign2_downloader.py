#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import requests
import feedparser
from bs4 import BeautifulSoup

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

FEED_URL = "https://feeds.simplecast.com/LXz4Q9rJ"
EP1_19_PAGE_URL = "https://critrole.com/podcast/campaign-2-ep1-ep51-mighty-nein-podcast/"
DOWNLOAD_FOLDER = "campaign2_mightynein"  # Established folder name

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def sanitize_filename(name: str) -> str:
    """Sanitize the filename by removing unwanted characters and replacing spaces with underscores."""
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def add_id3_tags(filepath: str, title: str):
    """Add ID3 tags to the downloaded MP3 file."""
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath)
    audio["title"] = title
    audio["artist"] = "Critical Role"
    audio["album"] = "Campaign 2: The Mighty Nein"
    audio.save()

def download_episode(mp3_url: str, title: str, folder: str):
    """Download the MP3 file, tag it, and save it to the specified folder."""
    filename = sanitize_filename(title) + ".mp3"
    filepath = os.path.join(folder, filename)
    if os.path.exists(filepath):
        print(f"   -> Already exists: {filename}")
        return
    try:
        with requests.get(mp3_url, headers=HEADERS, stream=True) as resp:
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        add_id3_tags(filepath, title)
        print(f"   -> Finished: {filepath}")
    except Exception as e:
        print(f"Error downloading '{title}': {e}")

def download_first19_from_page():
    """Download Campaign 2 episodes EP1–EP19 from the specified webpage with consistent naming."""
    print(f"Fetching page for EP1-EP51 from: {EP1_19_PAGE_URL}")
    response = requests.get(EP1_19_PAGE_URL, headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Ensure the download folder exists
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    # Pattern to match Campaign 2 episodes EP1 to EP19 in the link text
    ep_pattern = re.compile(r"Campaign 2,\s*EP([1-9]|1[0-9])\b", re.IGNORECASE)
    links = soup.find_all("a", href=True)

    downloaded_any = False
    for link in links:
        text = link.get_text()
        href = link["href"]
        # Check if link text matches EP1 to EP19 and if the URL contains '.mp3'
        if ep_pattern.search(text) and ".mp3" in href:
            # Transform title for consistent naming: "Campaign 2, EP1 Curious Beginnings" -> "C2E1 Curious Beginnings"
            m = re.match(r"Campaign 2,\s*EP(\d+)\s*(.*)", text, re.IGNORECASE)
            if m:
                ep_num = m.group(1)
                remainder = m.group(2)
                standardized_title = f"C2E{ep_num} {remainder}".strip()
            else:
                standardized_title = text.strip()

            print(f"Found episode: {standardized_title}")
            download_episode(href, standardized_title, DOWNLOAD_FOLDER)
            downloaded_any = True

    if not downloaded_any:
        print("No new episodes found on the page for EP1-EP19.")

def main():
    # First, attempt to download EP1-EP19 episodes from the webpage
    download_first19_from_page()

    # Continue with feed processing for remaining episodes (EP20+)
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    print(f"\nFetching feed from: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    episodes = feed.entries
    print(f"Found {len(episodes)} episodes in the feed.\n")

    downloaded_count = 0
    for idx, entry in enumerate(episodes, start=1):
        title = entry.title

        # Filter: Process only Campaign 2 episodes
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
            downloaded_count += 1
            print(f"   -> Finished: {filepath}")
        except Exception as e:
            print(f"   -> Error downloading '{title}': {e}")

    print(f"\nAll episodes processed. Total downloaded: {downloaded_count}")

if __name__ == "__main__":
    main()
