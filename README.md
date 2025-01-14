# Critical Role Podcast Downloaders

This repository contains four scripts (plus pre-built EXEs) to download Critical Role podcasts:

1. **Campaign 1: Vox Machina**
   - Episodes are downloaded directly from [critrole.com](https://critrole.com).

2. **Campaign 2: The Mighty Nein**
   - The first 19 episodes are pulled from [Critical Role's website](https://critrole.com/podcast/campaign-2-ep1-ep51-mighty-nein-podcast/).
   - From episode 20 onward, episodes are fetched via the Simplecast RSS feed: [https://feeds.simplecast.com/LXz4Q9rJ](https://feeds.simplecast.com/LXz4Q9rJ).
   - Episodes up to E20 are not available on the RSS feed, requiring this dual-source approach.

3. **Campaign 3: Bells Hells**
   - Episodes are fetched via the Simplecast RSS feed.
   - As of January 13, 2025, the campaign is ongoing. Incremental download support is included.
   - The script maintains a log of downloaded episodes in a `.txt` file, allowing re-runs to fetch new content without duplicating existing files.

4. **Special Episodes (e.g., One-Shots, 4-Sided Dive, etc.)**
   - Episodes are fetched via the Simplecast RSS feed with automated folder filtering.
   - The script includes the same incremental download functionality as Campaign 3.

---

## Table of Contents

- [Folder Overview](#folder-overview)
- [Usage Instructions (Scripts)](#usage-instructions-scripts)
- [Usage Instructions (EXEs)](#usage-instructions-exes)
- [Technical Details](#technical-details)
- [Known Issues](#known-issues)
- [Disclaimer](#disclaimer)

---

## Folder Overview

Each campaign and special episodes have separate folders containing their respective scripts and executables:

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
- Required packages: `requests`, `beautifulsoup4`, `mutagen`, `feedparser`

### Steps

1. **Download** the desired `.py` file (e.g., `critrole_campaign1_downloader.py`).
2. **Install dependencies** by running the following command in your terminal:
   ```bash
   pip install requests beautifulsoup4 mutagen feedparser
   ```
3. **Run the Script**:
   ```bash
   python critrole_campaign1_downloader.py
   ```
4. **Downloaded Files**: Episodes will be saved in a subfolder (e.g., `campaign1_voxmachina`).

### Notes

- **Campaign 3 and Specials** scripts can be re-run to fetch new episodes without re-downloading existing ones.
- Progress is tracked in a `.txt` file stored alongside the script. You can delete or edit this file to re-download episodes.
- The `.txt` file must remain in the same folder as the script or `.exe` to ensure proper functionality. However, you can move the audio files and folders freely.

---

## Usage Instructions (EXEs)

Each folder also contains a pre-built `.exe` (Windows only) for convenience. Simply double-click or run the `.exe` in a terminal:

```bash
./critrole_campaign1_downloader.exe
```

### Notes

- Windows SmartScreen or antivirus software may warn about unrecognized executables. Allow them only if you trust the source.
- The `.exe` will produce a console window displaying progress, including the number of episodes found and downloaded.

---

## Technical Details

- The Python scripts utilize the following libraries:
  - `requests` (HTTP library)
  - `beautifulsoup4` (HTML parsing)
  - `mutagen` (ID3 tag editing)
  - `feedparser` (RSS parsing)
- The Windows executables are built using:
  ```bash
  pyinstaller --onefile --console scriptname.py
  ```

---

## Known Issues

- **ID3 Tag Dates**: Some ID3 tag dates are derived from the source file attributes, which may incorrectly label an episode (e.g., a Campaign 1 episode as being from 2023).

---

## Disclaimer

This is an unofficial tool created for personal convenience. Ensure you adhere to Critical Role’s [Content Policy](https://critrole.com/critical-role-content-policy/) and comply with local laws regarding downloads and distribution.
