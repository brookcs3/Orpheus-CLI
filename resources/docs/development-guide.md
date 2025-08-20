# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

The Orpheus Collage Tools is a comprehensive command-line suite for searching, browsing, and downloading music releases from the Orpheus.network private tracker. The project combines web scraping with API calls to overcome limitations of the Orpheus API and provide detailed release information with precise download control.

## Architecture and Key Components

### Main Entry Point
- `collage_tools` - Main bash script providing interactive menu and command dispatching
- Executable entry point that routes to appropriate Python scripts based on user input

### Core Python Scripts
- `find_album_collages.py` - Primary album search, release parsing, and download functionality
  - Implements release-based organization (not format-based)
  - Handles interactive pagination and browsing
  - Combines web scraping + API integration for comprehensive data
- `download_collage_torrents.py` - Bulk downloading from collages with encoding preferences
- `download_crate.py` - Crate management system for organizing downloads
- `orpheus_cli.py` - Alternative CLI interface

### Authentication and Configuration
- `config.json` - Optional credentials storage (username, password, api_key)
- Fallback to hardcoded credentials in scripts if config not present
- Web login + API authentication hybrid approach

### Data Organization
- Release-based grouping by unique pressing characteristics (year|title|label|catalog|media)
- Torrents grouped under actual physical/digital releases, not just file formats
- Smart sorting: official releases first, compilations last

## Common Commands

### Interactive Mode (Primary Interface)
```bash
./collage_tools                    # Start interactive menu system
```

### Album Search Commands
```bash
# Basic artist search
./collage_tools find-album --artist "Artist Name" --interactive

# Official releases only (no compilations)
./collage_tools find-album --artist "Artist Name" --official-only --interactive

# Specific album search
./collage_tools find-album --artist "Artist Name" --album "Album Name"

# Show collage membership
./collage_tools find-album --artist "Artist Name" --show-collages

# Non-interactive output (for scripting)
./collage_tools find-album --artist "Artist Name" --all
```

### Download Commands (--prefer flag is mandatory)
```bash
# Download from collage with format preference
./collage_tools download [collage_id] --prefer-320   # MP3 320
./collage_tools download [collage_id] --prefer-v0    # MP3 V0 
./collage_tools download [collage_id] --prefer-flac  # FLAC
```

### Crate Management Commands
```bash
./collage_tools crate list                    # List existing crates
./collage_tools crate create "Crate Name"     # Create new crate
./collage_tools crate download "Crate Name"   # Download entire crate
```

### Quick Search
```bash
./collage_tools quick-search --artist "Artist" --album "Album"
```

## Interactive Mode Navigation

When using interactive mode, key commands include:
- `n` - Next album/page
- `t` - Toggle tracklist display
- `c` - Toggle collage membership display (when available)
- `q` - Quit program
- `h` - Return to main menu
- `s 150` - Skip to album number 150
- `d 1 a2` - Download album 1, format a2 (Release A, format 2)
- `1-16` - Filter by release type when filter menu shown
- `a` - Show all release types (remove filter)

## Download Selection Format

Downloads use alphabetical release + format coding:
```
Release A: 1997 | XL Recordings | XLCD 121 | CD
  [a1] FLAC Lossless | 562.0 MB | 17 seeders    # d 1 a1
  [a2] MP3 320 | 185.0 MB | 4 seeders           # d 1 a2

Release B: 1997 | UDP | UDP-D 77211 | CD  
  [b1] FLAC Lossless | 407.2 MB | 65 seeders    # d 1 b1
```

## Dependencies and Setup

### Required Dependencies
```bash
pip install aiohttp beautifulsoup4 click
```

### Configuration Setup
Create `~/.orpheus/config.json`:
```json
{
  "username": "your_username",
  "password": "your_password",
  "api_key": "your_api_key"
}
```

### Make Main Script Executable
```bash
chmod +x collage_tools
```

## Key Features

### Release-Based Organization
- Groups torrents by actual physical/digital releases
- Shows complete metadata: year, label, catalog number, media type
- All available formats displayed per release with seeder counts

### Hybrid Data Collection
- Web scraping for initial search and discovery
- API calls for detailed torrent group information  
- Combined processing for comprehensive release data

### Smart Search and Filtering
- Fuzzy matching for album/artist names
- Official releases vs. all releases filtering
- Release type filtering (Albums, EPs, Singles, etc.)
- Chronological sorting with official releases prioritized

### Interactive Browsing
- One album per page to avoid information overload
- Complete tracklist display (toggleable)
- Page-by-page navigation with skip functionality
- Collage membership information

## Next Steps and Planned Improvements

Based on user feedback and testing, the following improvements are planned:

### High Priority UX Improvements
1. **Allow artist-only search** - Option 2 (Find collages) should work with just artist name, not require both artist + album
2. **Improve navigation persistence** - Menu should stay visible/accessible throughout workflows  
3. **Better collage workflow integration** - Currently need to remember collage ID and return to main menu to download
4. **Numbered crate selection** - Replace typing crate names with number selection (1, 2, 3, etc.)
5. **Fix crate browsing** - Show crate contents without requiring artist search, paginate (2 albums per page)

### Feature Enhancements
6. **Track search functionality** - Search by track name + artist with fuzzy matching for misspellings
7. **Improved GUI visual design** - Better visual hierarchy, spacing, and formatting consistency
8. **Enhanced menu persistence** - Universal navigation menu available throughout all workflows

### Current App Strengths
- Release-based organization works excellently (e.g., 23 different pressings of "The Fat Of The Land")
- Collage discovery is powerful (shows membership in 21+ collages per album)
- Bulk download system is reliable (97.9% success rates for large collections)
- Interactive navigation with single-key commands (n/t/c/d/s/h) is intuitive

## File Structure

```
~/.orpheus/
├── collage_tools                    # Main executable bash script
├── config.json                     # → symlink to ~/.orpheus-config/config.json
├── requirements.txt                 # Python dependencies
├── lib/                            # Core functionality
│   ├── find_album_collages.py     # Core search functionality
│   ├── download_collage_torrents.py # Collage download functionality
│   ├── download_crate.py           # Crate management system
│   └── download_album_preferences.py # Core download functionality
└── resources/                      # Additional documentation and future features
    ├── docs/                       # Full documentation
    ├── mcp/                        # MCP server (planned integration)
    └── data/                       # User data
        └── crates/                 # User-created wishlists
            ├── Funk Masters.json
            ├── 90s Hip Hop Classics.json
            └── 25_forgotten_female_rap.json
```

## Testing and Development

No specific test framework is configured. The project relies on manual testing through the interactive interface and command-line operations.

### Reference Files
Development reference files (API responses, HTML examples) are stored in `resources/docs/reference_files/` but are excluded from git via `.gitignore`. These help understand API structures without exposing potentially large response files in the repository.

For development and debugging:
- All downloads save to `~/Downloads/` as `.torrent` files
- Scripts handle SSL certificate bypass for private tracker access
- Error handling includes graceful recovery and clear user messages
- Async architecture with session management for performance
- Crate system acts as wishlist/shopping cart for bulk operations