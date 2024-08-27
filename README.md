
## 全自动原神音乐（预下载）解包&分析工具
## Fully Automated Genshin Pre-Download Music Unpacking & Comparison Tool

### 功能

- **自动识别路径**：自动检测原神的安装路径，并复制游戏中的音乐文件。
- **预下载处理**：自动从米哈游官方接口下载原神新版本（预下载）的音乐文件，无须手动下载几十G的差分更新文件，免去了使用hdiff工具解密的过程。
- **自动提取比较**：脚本将自动提取音乐文件进行比较和去重并输出新增的音乐文件。
- 该脚本也可用于米家其他游戏及音频分析，前提是你需要知道Game_id和文件结构。

### 使用

1. 运行 `Main.py` 脚本，需要安装原神，否则必须手动复制音乐文件到Original Game Files文件夹，路径为\\Mihoyo\\Genshin Impact\\Genshin Impact Game\\YuanShen_Data\\StreamingAssets\\AudioAssets\\Music*.pck
2. 脚本将自动进行路径检测、文件复制、文件提取与对比分析。
3. `New Game Files` 为新版本的预下载音乐文件，`Original Game Files` 为旧版本的音乐文件，`WAV` 文件夹中为新增的音乐文件。


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
