# Orpheus MCP & CLI

**Intelligent torrent discovery and downloading for Orpheus with interactive MCP integration**

This project provides a comprehensive set of tools for interacting with the Orpheus music platform, including a powerful command-line interface (CLI) and an interactive MCP server.

## Features

- **Artist and Album Search:** Search for artists and albums, and view a list of available releases.
- **Collage Discovery:** Discover which collages an album belongs to using a hybrid web scraping and API approach.
- **Intelligent Downloading:** Download torrents from collages with smart encoding preferences and fallback options.
- **Offline Database:** Build and search an offline database of collage information for fast, efficient searching.
- **Interactive MCP:** Use the interactive MCP server to guide you through the process of searching for and downloading music.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd .orpheus
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your credentials:**

   Create a file named `config.json` in the root of the project directory with the following content:

   ```json
   {
     "username": "your_username",
     "password": "your_password",
     "api_key": "your_api_key"
   }
   ```

## Usage

### Interactive Mode (Primary Interface)

The main way to use the tools is through the interactive menu:

```bash
./collage_tools
```

This provides a guided interface with options for:
1. 🎤 Find artist albums & releases (with crates)
2. 🔍 Find which collages contain a specific album  
3. ⬇️ Download torrents from a collage
4. 📦 Manage crates
5. 🎯 Load crate and browse
6. ❌ Exit

### Command Line Interface

For direct commands and scripting:

```bash
# Search for artist releases
./collage_tools find-album --artist "The Prodigy" --interactive

# Download from collage (--prefer flag required)
./collage_tools download 6936 --prefer-flac

# Manage crates
./collage_tools crate list
./collage_tools crate create "My Collection"
```

### MCP Integration

MCP server functionality (future development):

```bash
python mcp/server.py
```

## Planned Improvements

### High Priority UX Improvements
1. **Allow artist-only search** - Find collages option should work with just artist name
2. **Improve navigation persistence** - Menu should stay accessible throughout workflows  
3. **Better collage workflow integration** - Streamline collage discovery → download process
4. **Numbered crate selection** - Replace typing crate names with number selection
5. **Fix crate browsing** - Show crate contents without requiring artist search

### Feature Enhancements  
6. **Track search functionality** - Search by track name + artist with fuzzy matching
7. **Improved GUI visual design** - Better visual hierarchy and formatting consistency
8. **Enhanced menu persistence** - Universal navigation available in all workflows

### Current Strengths
- **Release-based organization** - Groups by actual pressings/labels, not just file formats
- **Powerful collage discovery** - Shows membership across dozens of curated collections
- **Reliable bulk downloads** - 97%+ success rates for large collection downloads
- **Intuitive navigation** - Single-key commands (n/t/c/d/s/h) for efficient browsing