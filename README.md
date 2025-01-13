# Critical Role Podcast Downloaders

This repository contains four scripts (plus pre-built EXEs) to download
the Critical Role podcasts:

1. **Campaign 1: Vox Machina**

    directly from critrole.com
2. **Campaign 2: The Mighty Nein**
    
    The first 19 Episodes are pulled via https://critrole.com/podcast/campaign-2-ep1-ep51-mighty-nein-podcast/ 
    from C2E20 on they're fetched over the simplecast RSS Feed https://feeds.simplecast.com/LXz4Q9rJ
    since critrole.com is inconsistent with their Podcast implementation.
3. **Campaign 3: Bells Hells**

    Also fetched via simplecast RSS.
    The Campaign at present date (13.01.25) is still ongoing, so there is incremental download support.
    The script will check via .txt file if it has already downloaded Episodes and skip those,
    therefore you can just re-run it to catch new ones.
4. **Special Episodes like One-Shots, 4-Sided Dive etc**
    
    Also fetched via simplecast RSS.
    With automated folder-filtering. YMMV!
    Same "memory" behaviour as the C3 script, so you can re-run to fetch new Epidsodes.

---

## Table of Contents

- [Folder Overview](#folder-overview)
- [Usage Instructions (Scripts)](#usage-instructions-scripts)
- [Usage Instructions (EXEs)](#usage-instructions-exes)
- [Technical Details](#technical-details)
- [Disclaimer](#disclaimer)

---

## Folder Overview

- **Campaign1/**
  - `critrole_campaign1_downloader.py`  
  - `critrole_campaign1_downloader.exe`
- **Campaign2/**
  - `critrole_campaign2_downloader.py`  
  - `critrole_campaign2_downloader.exe`
- **Campaign3/**
  - `critrole_campaign3_downloader.py`  
  - `critrole_campaign3_downloader.exe`
- **Special Episodes/**
  - `critrole_specials_downloader.py`  
  - `critrole_specials_downloader.exe`

---

## Usage Instructions (Scripts)

### Requirements
- Python 3.x
- `requests`, `beautifulsoup4`, `mutagen`, `feedparser` packages

### Steps
1. **Download** the `.py` file you want (e.g., `critrole_campaign1_downloader.py`).
2. **Install dependencies** (in a terminal):
      pip install requests beautifulsoup4 mutagen feedparser
3. **Run the Script**: 
   for example "python critrole_campaign1_downloader.py"
4. **The episodes will be downloaded into a subfolder (e.g. campaign1_voxmachina).**

**Campaign 3 and Specials** script can be re-run in the future to grab any new episodes without re-downloading old ones.
Progress is saved in a corresponding .txt file which you can delete or edit at will if you want to download completely again for example.
The .txt must remain together with the .exe to check for already downloaded episodes, the folders and audiofiles however can be moved at will.



**Usage Instructions (EXEs)**

Each folder also contains a pre-built .exe (Windows only) that you can run without installing Python. Just double-click or run it in terminal:

.\critrole_campaign1_downloader.exe


    Note: Windows SmartScreen or antivirus might warn about unrecognized .exe; you can allow it if you trust these files.
    Also: The .exe might produce a console window. You’ll see output about how many episodes are found, etc.

Technical Details

    Python scripts use:
        requests (HTTP library)
        BeautifulSoup (HTML parsing)
        mutagen (ID3 tags)
        feedparser (RSS parsing)
    For Windows EXE creation, I used: 
        pyinstaller --onefile --console scriptname.py




**Disclaimer**

This is an unofficial tool created for personal convenience.
Make sure you follow Critical Role’s Content Policy (https://critrole.com/critical-role-content-policy/) and local laws regarding downloads & distribution.
