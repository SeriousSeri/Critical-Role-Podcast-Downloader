#!/usr/bin/env python3
import feedparser
import os
import requests
import re

# URL of the Simplecast feed
FEED_URL = "https://feeds.simplecast.com/LXz4Q9rJ"

# Base folder where episodes will be saved
DOWNLOAD_FOLDER = "special_episodes"

# Compile a regular expression to identify campaign episode codes 
# Allow optional whitespace between campaign identifier and episode number.
campaign_regex = re.compile(r"C[123]\s*E\d+", re.IGNORECASE)

def sanitize_filename(name: str) -> str:
    """
    Sanitize the filename by removing unwanted characters
    and replacing spaces with underscores.
    """
    name = re.sub(r"[^a-zA-Z0-9\s\-_\.]+", "", name)
    name = re.sub(r"\s+", "_", name)
    return name.strip()

def main():
    print(f"Fetching feed from: {FEED_URL}")
    feed = feedparser.parse(FEED_URL)
    total = len(feed.entries)
    print(f"Found {total} episodes in the feed.")

    # Use 'downloaded_specials.txt' to track downloaded episodes
    downloaded_db_file = "downloaded_specials.txt"
    downloaded = set()
    if os.path.exists(downloaded_db_file):
        with open(downloaded_db_file, "r", encoding="utf-8") as f:
            for line in f:
                downloaded.add(line.strip())

    idx = 1
    for entry in feed.entries:
        title = entry.title

        # Filter: Skip if title contains a campaign episode code and not part of "4-Sided Dive"
        if campaign_regex.search(title) and "4-Sided Dive" not in title:
            print(f"[{idx}] Skipping Campaign episode: '{title}'")
            idx += 1
            continue

        # Skip if we've already downloaded this episode
        if title in downloaded:
            print(f"[{idx}] Already downloaded: '{title}'")
            idx += 1
            continue

        # Determine destination folder based on title keywords
        folder = "Misc"  # Default folder
        if "One-Shot" in title:
            folder = "One-Shot"
        elif "Critical Role Presents" in title:
            folder = "Critical Role Presents"
        elif "4-Sided Dive" in title:
            folder = "4-Sided Dive"
        # Add more conditions as needed for other series

        # Ensure the destination folder exists
        folder_path = os.path.join(DOWNLOAD_FOLDER, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Check for an MP3 enclosure in the feed entry
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

                # Mark this episode as downloaded
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
