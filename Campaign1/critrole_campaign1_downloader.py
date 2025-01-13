#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import requests
from bs4 import BeautifulSoup

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

URL_CAMPAIGN1 = "https://critrole.com/campaign-1-podcast/"
DOWNLOAD_FOLDER = "campaign1_voxmachina"

# User-Agent to avoid 403 blocks
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def fetch_campaign1_page():
    resp = requests.get(URL_CAMPAIGN1, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_mp3_links(html_text: str) -> list:
    soup = BeautifulSoup(html_text, "html.parser")
    results = []
    # Find all <a> tags with href containing ".mp3"
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".mp3" in href.lower():
            link_text = a.get_text(strip=True)
            if not link_text:
                link_text = os.path.basename(href)
            results.append((link_text, href))
    return results

def add_id3_tags(filepath: str, title: str):
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath)

    audio["title"] = title
    audio["artist"] = "Critical Role"
    audio["album"] = "Campaign 1: Vox Machina"
    audio.save()

def main():
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    html_text = fetch_campaign1_page()
    episodes = parse_mp3_links(html_text)

    print(f"Gefundene Episoden-Links: {len(episodes)}")
    for idx, (episode_title, mp3_url) in enumerate(episodes, start=1):
        # Extract episode number and subtitle to format as "C1E<number>_<Subtitle>"
        match = re.search(r"EP\s*(\d+)\s*(.*)", episode_title, re.IGNORECASE)
        if match:
            ep_num = match.group(1)
            remainder = match.group(2).strip()
            # Remove any leading non-alphanumeric characters from the subtitle
            remainder = re.sub(r"^[^a-zA-Z0-9]+", "", remainder)
            if remainder:
                standardized_title = f"C1E{ep_num}_{remainder}"
            else:
                standardized_title = f"C1E{ep_num}"
        else:
            standardized_title = f"C1_{episode_title}"

        filename = sanitize_filename(standardized_title) + ".mp3"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        if os.path.exists(filepath):
            print(f"[{idx}] EXISTIERT BEREITS: {filename} - Überspringe.")
            continue

        print(f"[{idx}] Lade herunter: {episode_title} => {filename}")

        resp = requests.get(mp3_url, headers=HEADERS, stream=True)
        resp.raise_for_status()

        with open(filepath, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"   -> Fertig: {filepath}")
        # Replace underscores with spaces for the ID3 tag title
        add_id3_tags(filepath, standardized_title.replace("_", " "))

    print("\nAlle Episoden wurden verarbeitet.")

if __name__ == "__main__":
    main()
