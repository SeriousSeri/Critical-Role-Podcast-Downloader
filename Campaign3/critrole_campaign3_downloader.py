#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import time
import requests
from bs4 import BeautifulSoup

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

BASE_URL = "https://critrole.com"
START_URL = "https://critrole.com/podcastfilter/campaign-3/"
DOWNLOAD_FOLDER = "campaign3_bellshells"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

def sanitize_filename(name: str) -> str:
    """
    Ersetzt unzulässige Zeichen und wandelt Leerzeichen in Unterstriche um.
    """
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def get_soup(url: str) -> BeautifulSoup:
    """
    Lädt eine URL (mit HEADERS) und gibt ein BeautifulSoup-Objekt zurück.
    """
    time.sleep(1)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def find_episode_listings(soup: BeautifulSoup) -> list:
    """
    Sucht auf der Übersichtsseite nach Episoden-Einträgen.
    Gibt Liste der Detail-Links zurück (z. B. /podcast/...).
    """
    episode_divs = soup.find_all("div", class_="qt-part-archive-item qt-item-podcast")
    links = []
    for div in episode_divs:
        a_tag = div.find("a", class_="qt-text-shadow", href=True)
        if a_tag:
            links.append(a_tag["href"])
    return links

def find_next_page(soup: BeautifulSoup) -> str:
    """
    Sucht <link rel="next" href="...">, um paginierte Folgeseite zu finden.
    """
    next_link = soup.find("link", rel="next")
    if next_link and "href" in next_link.attrs:
        return next_link["href"]
    return None

def parse_episode_page(url: str) -> (str, str):
    """
    Lädt die Seite einer Episode und extrahiert
     - den Episodentitel
     - den eigentlichen MP3-Link
    """
    s = get_soup(url)
    # Titel
    title_tag = s.find(["h1", "h4"], class_="qt-ellipsis-2")
    if title_tag:
        episode_title = title_tag.get_text(strip=True)
    else:
        if s.title:
            episode_title = s.title.get_text(strip=True)
        else:
            episode_title = "Unknown Episode"

    # MP3-Link: check <audio src> oder <a href="...mp3">
    mp3_url = None
    audio_tag = s.find("audio", src=True)
    if audio_tag:
        mp3_url = audio_tag["src"]
    else:
        for a in s.find_all("a", href=True):
            if ".mp3" in a["href"].lower():
                mp3_url = a["href"]
                break

    return (episode_title, mp3_url)

def add_id3_tags(filepath: str, episode_title: str):
    """
    ID3-Tags: Title, Artist=Critical Role, Album=Campaign 3: Bells Hells.
    """
    try:
        audio = EasyID3(filepath)
    except ID3NoHeaderError:
        audio = EasyID3()
        audio.save(filepath)

    audio["title"] = episode_title
    audio["artist"] = "Critical Role"
    audio["album"] = "Campaign 3: Bells Hells"
    audio.save()

def download_mp3(mp3_url: str, episode_title: str, existing_files: set):
    """
    Lädt die MP3 herunter (falls nicht schon existiert) und setzt ID3-Tags.
    """
    if not mp3_url:
        print(f"    Kein MP3-Link für '{episode_title}'. Überspringe.")
        return

    filename = sanitize_filename(f"C3_{episode_title}") + ".mp3"
    if filename in existing_files:
        print(f"    Datei {filename} existiert bereits (Set). Überspringe.")
        return

    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        print(f"    Datei {filename} existiert bereits. Überspringe.")
        existing_files.add(filename)
        return

    print(f"    Lade herunter: {filename}")
    resp = requests.get(mp3_url, headers=HEADERS, stream=True)
    resp.raise_for_status()

    with open(filepath, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    print(f"    -> Fertig: {filepath}")
    # ID3
    add_id3_tags(filepath, episode_title)
    # In die Set-Liste einfügen
    existing_files.add(filename)

def main():
    # Ordner anlegen, falls nicht existiert
    if not os.path.isdir(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    # Liste der bereits vorhandenen Dateien einlesen
    existing_files = {
        fn for fn in os.listdir(DOWNLOAD_FOLDER) if fn.lower().endswith(".mp3")
    }

    current_url = START_URL
    page_num = 1

    while current_url:
        print(f"Scanne Seite {page_num}: {current_url}")
        soup = get_soup(current_url)

        episode_links = find_episode_listings(soup)
        print(f"  -> Gefundene Episoden: {len(episode_links)}")

        for link in episode_links:
            if not link.startswith("http"):
                link = BASE_URL + link
            # Seite parsen
            title, mp3_link = parse_episode_page(link)
            print(f"  Episodentitel: {title}")
            download_mp3(mp3_link, title, existing_files)

        # nächste Seite
        next_page = find_next_page(soup)
        if next_page:
            current_url = next_page
            page_num += 1
        else:
            break

    print("\nAlle verfügbaren Episoden verarbeitet - neue Downloads abgeschlossen!")

if __name__ == "__main__":
    main()
