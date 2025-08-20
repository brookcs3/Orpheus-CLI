# Orpheus Collage Tools - User Documentation

A comprehensive command-line suite for searching, browsing, and downloading music releases from the Orpheus.network private tracker.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Interactive Mode (Human Users)](#interactive-mode-human-users)
- [Command Line Mode (AI/Automation)](#command-line-mode-aiautomation)
- [Features Overview](#features-overview)
- [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.7+
- BeautifulSoup4 and aiohttp Python packages
- Valid Orpheus.network account credentials

### Setup
```bash
# Install required Python packages
pip3 install beautifulsoup4 aiohttp

# Navigate to the Orpheus tools directory
cd ~/.orpheus

# Make the main script executable
chmod +x collage_tools
```

### Configuration (Optional)
Create a `config.json` file in `~/.orpheus/`:
```json
{
  "username": "your_orpheus_username",
  "password": "your_orpheus_password",
  "api_key": "your_orpheus_api_key"
}
```

---

## Quick Start

### Interactive Mode (Recommended for Humans)
Simply run the tool without arguments:
```bash
./collage_tools
```

### Command Mode (For Scripts/AI)
```bash
./collage_tools find-album --artist "The Prodigy" --interactive
```

---

## Interactive Mode (Human Users)

### Main Menu
When you run `./collage_tools`, you'll see:
```
🎵 Orpheus Collage Tools - Interactive Mode
==========================================

What would you like to do?
1. 🎤 Find artist albums & releases
2. 🔍 Find which collages contain a specific album
3. ⬇️  Download torrents from a collage
4. ❌ Exit
```

### Option 1: Find Artist Albums & Releases

#### Step 1: Choose Search Type
After selecting option 1 and entering an artist name:
```
🎵 Release search options:
1. All releases (including compilations)
2. Official releases only
3. Search specific release
```

#### Step 2: Browse Results
You'll see one album per page with complete details:
```
1. Portishead — Dummy
════════════════════════════════════════════════════════════
🔄  Loading release details...! 📚 In 20 collage(s)...press c to show
📅  Year: 1994
💿  Available Releases (5):

   • Release A: 1994 | Go! Beat | 828 522-2 | CD
     [a1] FLAC Lossless        |   244.0 MB |  65 seeders
     [a2] MP3 320              |    89.8 MB |  12 seeders
     [a3] MP3 V0 (VBR)         |    73.2 MB |   8 seeders

   • Release B: 2011 | Go! Beat | 0602527867656 | Vinyl
     [b1] FLAC 24bit Lossless  |   562.3 MB |  43 seeders
     [b2] FLAC Lossless        |   245.1 MB |  28 seeders
════════════════════════════════════════════════════════════
🎵  TRACKLIST (11 tracks): Press 't' to view
════════════════════════════════════════════════════════════
```

#### Navigation Commands
```
🎯  Options:
   n = Next release | t = Show tracks | q = Quit
   d <#> <fmt> = Download (e.g. 'd 1 a2') | c = Show collages
   skip to page (s <#>) to go to page # of 195 | h = Home (main menu)
```

- **n** - Go to next album
- **t** - Toggle track list display
- **c** - Toggle collage list display (if album is in collages)
- **q** - Quit to command line
- **h** - Return to main menu
- **s 50** - Skip to album #50
- **d 1 a2** - Download album 1, format a2 (MP3 320 from Release A)
- **1-16** - Filter by release type (when filter options shown)
- **a** - Show all release types (when filtered)

### Option 2: Find Collages for an Album
Enter both artist and album name to see which collages contain that specific album.

### Option 3: Download from Collage
Enter a collage ID and choose your preferred format:
- MP3 320 CBR
- MP3 V0 VBR  
- FLAC Lossless

---

## Command Line Mode (AI/Automation)

### Basic Album Search
```bash
# Search all releases by artist
./collage_tools find-album --artist "The Prodigy"

# Search official releases only
./collage_tools find-album --artist "The Prodigy" --official-only

# Search for specific album
./collage_tools find-album --artist "The Prodigy" --album "Experience"

# Interactive browsing mode
./collage_tools find-album --artist "The Prodigy" --interactive

# Show all results (no limit)
./collage_tools find-album --artist "The Prodigy" --all

# Limit results
./collage_tools find-album --artist "The Prodigy" --limit 20
```

### Advanced Search Options
```bash
# Show collage membership
./collage_tools find-album --artist "The Prodigy" --show-collages

# Combine multiple options
./collage_tools find-album --artist "Radiohead" --official-only --show-collages --interactive

# Search by album name only
./collage_tools find-album --album "OK Computer"
```

### Download from Collage
```bash
# Download with MP3 320 preference
./collage_tools download 6936 --prefer-320

# Download with FLAC preference
./collage_tools download 6936 --prefer-flac

# Download with MP3 V0 preference
./collage_tools download 6936 --prefer-v0
```

### Quick Search
```bash
# Find collages containing a specific album
./collage_tools quick-search --artist "Portishead" --album "Dummy"
```

---

## Features Overview

### 1. Release-Based Organization
Albums are grouped by actual physical/digital releases, not just file formats. Each release shows:
- Year (including remaster year)
- Record label
- Catalog number
- Media type (CD, Vinyl, WEB, etc.)
- All available formats with seeders

### 2. Interactive Features
- **Page Navigation**: Browse one album at a time
- **Skip to Page**: Jump directly to any album number
- **Track Toggle**: Show/hide complete tracklists
- **Collage Toggle**: Show/hide collage membership
- **Home Function**: Return to main menu anytime
- **Filter by Type**: Filter by Albums, EPs, Singles, etc.

### 3. Download System
- **Precise Selection**: Choose exact release and format (e.g., "d 1 b2")
- **Auto-naming**: Downloads saved as "Artist - Album [Format].torrent"
- **Location**: All torrents saved to ~/Downloads/

### 4. Smart Search
- **Fuzzy Matching**: "Fat of the land" finds "The Fat Of The Land"
- **Comprehensive Results**: Uses artist API for complete discographies
- **Intelligent Sorting**: Official releases prioritized, compilations last

---

## Command Reference

### Interactive Mode Commands
| Command | Action | Example |
|---------|--------|---------|
| n | Next album | `n` |
| t | Toggle tracks | `t` |
| c | Toggle collages | `c` |
| q | Quit program | `q` |
| h | Home (main menu) | `h` |
| s [num] | Skip to page | `s 150` |
| d [album] [format] | Download | `d 1 a2` |
| [number] | Filter by type | `1` (Albums) |
| a | Show all types | `a` |

### Command Line Flags
| Flag | Description | Example |
|------|-------------|---------|
| --artist | Artist name | `--artist "The Prodigy"` |
| --album | Album name | `--album "Experience"` |
| --interactive | Interactive mode | `--interactive` |
| --official-only | Skip compilations | `--official-only` |
| --show-collages | Show collages | `--show-collages` |
| --all | Show all results | `--all` |
| --limit N | Limit results | `--limit 20` |
| --prefer-320 | MP3 320 for downloads | `--prefer-320` |
| --prefer-v0 | MP3 V0 for downloads | `--prefer-v0` |
| --prefer-flac | FLAC for downloads | `--prefer-flac` |

---

## Troubleshooting

### Common Issues

1. **Login Failed**
   - Check credentials in config.json or hardcoded values
   - Ensure your Orpheus account is active

2. **No Results Found**
   - Try different search terms
   - Check artist spelling
   - Remove special characters

3. **Download Failed**
   - Verify the release format exists
   - Check your Orpheus download privileges
   - Ensure you're not rate-limited

4. **SSL Certificate Errors**
   - The tool bypasses SSL verification for private trackers
   - This is normal and expected behavior

### Debug Mode
For troubleshooting, you can see more details by checking the Python output directly:
```bash
python3 ~/.orpheus/find_album_collages.py --artist "Test" --interactive
```

---

## Examples

### Human User Workflow
1. Run `./collage_tools`
2. Choose option 1
3. Enter "Radiohead"
4. Choose option 2 (Official releases only)
5. Press 'n' to browse albums
6. Press 't' to see tracks
7. Type 'd 1 a1' to download FLAC version
8. Press 'h' to return to main menu

### AI/Automation Workflow
```bash
# Find all Radiohead albums, official only, with collages, interactive mode
./collage_tools find-album --artist "Radiohead" --official-only --show-collages --interactive

# Download all torrents from "Best of 90s" collage with FLAC preference
./collage_tools download 1234 --prefer-flac

# Quick check which collages have "OK Computer"
./collage_tools quick-search --artist "Radiohead" --album "OK Computer"
```

---

## Tips & Best Practices

1. **For Large Discographies**: Use `s [number]` to jump around quickly
2. **For Specific Formats**: Check seeders before downloading
3. **For Collage Downloads**: Always specify --prefer flag
4. **For Automation**: Use exit codes to check success/failure
5. **For Best Results**: Keep searches simple and specific

---

## Version History
- Current Version: Release-based organization with enhanced interactive features
- Supports: Full Orpheus API integration with web scraping fallback
- Platform: Linux/macOS with bash and Python 3.7+
