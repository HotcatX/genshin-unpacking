
---

## Fully Automated Genshin Pre-Download Music Unpacking & Comparison Tool

### Features

- **Automatic Path Detection**: Automatically detects Genshin Impact's installation path and copies the game’s music files.
- **Automatic Pre-Download Processing**: Automatically downloads the new version’s (pre-download) music files, extracts them, deduplicates, and outputs the new music files.
- **Automatic Extraction & Comparison**: No need to manually download several gigabytes of differential update files or use the `hdiff` tool—the script automatically compares and deduplicates the files.
- The script can also be used for other miHoYo games and audio analysis, provided you know the `Game_id` and file structure.

### Usage

1. Run the `Main.py` script. You need to have Genshin Impact installed; otherwise, you must manually copy the music files into the `Original Game Files` folder. The path is:  
   `\\Mihoyo\\Genshin Impact\\Genshin Impact Game\\YuanShen_Data\\StreamingAssets\\AudioAssets\\Music*.pck`
2. The script will automatically detect paths, copy files, extract, and compare the music files.
3. The `New Game Files` directory will contain the new pre-download music files, the `Original Game Files` directory will contain the old version music files, and the `WAV` folder will contain the new music files.

--- 
