# Critical Role Podcast Downloaders

This repository contains three scripts (plus pre-built EXEs) to download
the Critical Role podcasts:

1. **Campaign 1: Vox Machina**  
2. **Campaign 2: The Mighty Nein**  
3. **Campaign 3: Bells Hells** (ongoing, with incremental download support)

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

---

## Usage Instructions (Scripts)

Technical sidenote: Trying to be nice, the scripts implement an incremental download of episodes with small pauses in between them to not wreak havoc on their servers. 
Therefore the download of whole campaigns will take longer than you would probably expect in regards of your bandwith.

### Requirements
- Python 3.x
- `requests`, `beautifulsoup4`, `mutagen` packages

### Steps
1. **Download** the `.py` file you want (e.g., `critrole_campaign1_downloader.py`).
2. **Install dependencies** (in a terminal):
   ```bash
   pip install requests beautifulsoup4 mutagen
3. **Run the Script**: 
   python critrole_campaign1_downloader.py
4. **The episodes will be downloaded into a subfolder (e.g. campaign1_voxmachina).**

**Campaign 3** script can be re-run in the future to grab any new episodes without re-downloading old ones.



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
    For Windows EXE creation, I used:

pyinstaller --onefile --console scriptname.py


**Disclaimer**

This is an unofficial tool created for personal convenience.
Make sure you follow Critical Role’s Content Policy (https://critrole.com/critical-role-content-policy/) and local laws regarding downloads & distribution.
