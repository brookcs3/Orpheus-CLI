# Orpheus Collage Tools - Project Status & Documentation

## 📋 Project Overview

**Orpheus Collage Tools** is a comprehensive command-line suite for searching, browsing, and downloading music releases from the Orpheus.network private tracker. The project solves key limitations of the Orpheus API by combining web scraping with API calls to provide detailed release information and precise download control.

### 🎯 Core Purpose
- **Search artist discographies** with comprehensive release details
- **Browse releases by actual pressings** (not just file formats)
- **Download specific torrent files** with precise selection control
- **Overcome API limitations** through intelligent web scraping

---

## 🏗️ Project Architecture

### Main Components

#### 1. `collage_tools` (Bash Script)
- **Location**: `~/.orpheus/collage_tools`
- **Purpose**: Main interactive menu system and command dispatcher
- **Executable**: `chmod +x` required

**Interactive Menu Options:**
1. 🎤 **Find artist albums & releases** - Main album search functionality
2. 🔍 **Find which collages contain an album** - Collage membership lookup
3. ⬇️ **Download torrents from a collage** - Bulk collage downloads
4. ❌ **Exit**

#### 2. `find_album_collages.py` (Python Script)
- **Location**: `~/.orpheus/find_album_collages.py`
- **Purpose**: Core album search, release parsing, and download functionality
- **Key Features**:
  - Web scraping + API integration
  - Release-based organization
  - Interactive pagination
  - Direct torrent downloading

#### 3. `download_collage_torrents.py` (Not Detailed)
- **Status**: Referenced but not implemented in our conversations
- **Purpose**: Bulk downloading from collages with encoding preferences

---

## ✨ Key Features Implemented

### 🔍 Advanced Search System
- **Fuzzy matching**: "Fat of the land" finds "The Fat Of The Land"
- **Multiple search modes**:
  - All albums (including compilations)
  - Official releases only
  - Specific album search
- **Smart sorting**: Official releases first, compilations last

### 🎵 Release-Based Organization
**Revolutionary change from format-based to release-based grouping:**

```
Release A: 1997 | XL Recordings | XLCD 121 | CD
  [a1] FLAC Lossless | 562.0 MB | 17 seeders
  [a2] MP3 320 | 185.0 MB | 4 seeders
  [a3] MP3 V0 | 145.0 MB | 8 seeders

Release B: 1997 | UDP | UDP-D 77211 | CD  
  [b1] FLAC Lossless | 407.2 MB | 65 seeders
  [b2] MP3 V0 | 110.2 MB | 17 seeders
```

### 📊 Comprehensive Metadata Display
- **Release Information**: Year, remaster title, record label, catalog number, media type
- **Format Details**: Encoding quality, file size, seeder count
- **Complete Tracklists**: All tracks numbered and listed
- **Visual Clarity**: Clear separation between releases and tracklists

### 🎯 Precise Download Control
- **Alphabetical Selection**: `d 1 a2` downloads format [a2] from album #1
- **Specific Targeting**: Choose exact pressing + format combination
- **Auto-naming**: Saves as `Artist - Album [Format].torrent`
- **Download Location**: `~/Downloads/`

### 🖥️ Interactive Interface
- **1 album per page**: See ALL releases without truncation
- **Simple navigation**: 'n' = next, 'q' = quit, 'd 1 a2' = download
- **Page-by-page browsing**: Never overwhelmed with too much information
- **Graceful error handling**: Clear error messages and recovery

---

## 🔧 Technical Implementation

### Authentication System
- **Web login**: Username/password for web scraping
- **API authentication**: Token-based for torrent group details
- **Config file**: `~/.orpheus/config.json` (optional)
- **Fallback**: Hardcoded credentials in script

### Hybrid Data Collection
1. **Web scraping** (BeautifulSoup): Initial album search and discovery
2. **API calls** (aiohttp): Detailed torrent group information
3. **Combined processing**: Merge web + API data for complete picture

### Release Grouping Algorithm
```python
# Groups torrents by unique release characteristics
release_key = f"{remaster_year}|{remaster_title}|{remaster_label}|{remaster_catalog}|{media}"
```

### Async Architecture
- **Concurrent API calls**: Fast data retrieval
- **Session management**: Persistent authentication
- **SSL bypass**: Works with private tracker certificates

---

## 📦 Dependencies & Requirements

### Required Dependencies
```bash
pip3 install beautifulsoup4 aiohttp
```

### Built-in Python Modules (No Installation Required)
- `asyncio` - Async programming
- `json` - Configuration and API parsing
- `re` - Pattern matching and text processing
- `argparse` - Command-line argument parsing
- `ssl` - SSL context management
- `pathlib` - File path handling
- `sys` - System-specific parameters

### System Requirements
- **Python 3.7+**: Async/await syntax
- **Internet connection**: Access to Orpheus.network
- **Valid Orpheus account**: Username, password, and API key

---

## 📁 File Structure

```
~/.orpheus/
├── collage_tools              # Main executable bash script
├── find_album_collages.py     # Core Python functionality
├── download_collage_torrents.py  # [Referenced but not implemented]
└── config.json               # [Optional] Credentials storage
```

### Configuration File Format (`config.json`)
```json
{
  "username": "your_username",
  "password": "your_password", 
  "api_key": "your_api_key_here"
}
```

---

## 🚀 Current Status & Capabilities

### ✅ Fully Implemented
- ✅ Interactive menu system
- ✅ Artist album search (all albums, official only, specific)
- ✅ Release-based organization with complete metadata
- ✅ Alphabetical selection system (a1, b1, c2, etc.)
- ✅ Complete tracklist display
- ✅ Direct torrent downloading
- ✅ Fuzzy search matching
- ✅ 1 album per page browsing
- ✅ Collage membership display (optional)
- ✅ Smart album sorting and filtering

### 🔄 Partially Implemented
- 🔄 Bulk collage downloading (referenced but not detailed)
- 🔄 Non-interactive batch operations (basic implementation)

### ❌ Not Part of This Project
- ❌ Actual music file downloading (only .torrent files)
- ❌ Torrent client integration
- ❌ Music library management
- ❌ Orpheus account management
- ❌ Other Orpheus features (forums, user stats, etc.)

---

## 💡 Recent Major Improvements

### 1. Release-Based Organization (Game Changer)
**Before**: Grouped by format quality (FLAC, MP3 320, etc.)
**After**: Grouped by actual releases with all formats shown per release

### 2. Enhanced Album Search Options
- Added "Search specific album" option
- Improved fuzzy matching
- Better search result filtering

### 3. Complete Tracklist Display
**Before**: "Sample Tracks: Track1, Track2... and 5 more tracks"
**After**: Complete numbered tracklist with clear visual separation

### 4. Improved Download Interface
- Changed from numeric IDs to alphabetical (a1, b2, c3)
- More intuitive selection system
- Better error messages

### 5. Visual Enhancements
- Clear separation between releases and tracklists
- Comprehensive metadata display
- Better pagination feedback

---

## 🎯 Usage Examples

### Basic Artist Search
```bash
./collage_tools
# Choose: 1 (Find artist albums & releases)
# Enter: The Prodigy
# Choose: 2 (Official releases only)
# Browse with 'n', download with 'd 1 a2'
```

### Specific Album Search
```bash
./collage_tools
# Choose: 1 (Find artist albums & releases)  
# Enter: The Prodigy
# Choose: 3 (Search specific album)
# Enter: Fat of the land
# Download with 'd 1 b1'
```

### Command Line Usage
```bash
# Direct album search
./collage_tools find-album --artist "The Prodigy" --interactive

# Official releases only
./collage_tools find-album --artist "The Prodigy" --official-only --interactive

# Specific album with collages
./collage_tools find-album --artist "The Prodigy" --album "Experience" --show-collages
```

---

## 🚨 Critical Development Principles

### **STRICT NO PLACEHOLDER/NO ASSUMPTION RULE**
**This project follows a zero-tolerance policy for placeholder data or endpoint assumptions.**

- ❌ **NO** made-up API responses
- ❌ **NO** assumed endpoint structures  
- ❌ **NO** placeholder JSON examples
- ✅ **ONLY** real data from actual API calls
- ✅ **ONLY** verified endpoint structures
- ✅ **ONLY** tested and working implementations

### **Primary Documentation Sources**

#### 1. Official API Documentation
**Location**: `/Users/cameronbrooks/Gazelle/docs/07-API.md`
- Complete Gazelle/Orpheus API reference
- Authoritative source for endpoint specifications
- Parameter definitions and response formats

#### 2. Real Endpoint Data Examples  
**Location**: `/Users/cameronbrooks/.orpheus/collage_6936_Sampled by The Prodigy/torrent_info.json`
- **CRITICAL RESOURCE**: Actual JSON responses from live API calls
- Real torrent group structure and metadata
- Authentic field names, data types, and nested objects
- **Use this as the source of truth** for understanding available data

#### 3. Live API Testing
- All endpoint usage must be verified through actual API calls
- Response structures must be validated with real data
- Field availability confirmed through multiple examples

### **Development Methodology**
1. **Research actual endpoints** using documentation
2. **Test with real API calls** to verify structure  
3. **Examine real JSON responses** like the torrent_info.json example
4. **Implement based on verified data** - never assumptions
5. **Validate with multiple real examples** before considering complete

---

## 🎨 Formatting & Styling Standards

### **Visual Design Principles**
- **Clean, scannable output**: Information hierarchy with proper spacing
- **Emoji indicators**: Consistent use for quick visual parsing
- **Tabular alignment**: Proper spacing for release metadata
- **Clear separation**: Blank lines between logical sections
- **Professional presentation**: Command-line tool should feel polished

### **User Experience Patterns**
- **Progressive disclosure**: 1 album per page, complete but not overwhelming
- **Intuitive commands**: Single letters ('n', 'q') for common actions
- **Logical grouping**: Releases organized by actual pressings, not arbitrary categories
- **Immediate feedback**: Loading indicators, clear success/error messages
- **Consistent formatting**: Same layout patterns throughout the application

### **Data Presentation Standards**
- **Complete information**: Show all available data, don't truncate arbitrarily
- **Meaningful organization**: Group related information logically
- **Clear selection methods**: Alphabetical indexing (a1, b2) for easy reference
- **Contextual details**: Include all relevant metadata for informed decisions

---

## 🚀 Project Roadmap & Goals

### **Ultimate Objective**
**Two-Phase Development Plan:**

#### **Phase 1: Comprehensive CLI Application** (Current Focus)
- Complete feature-rich command-line interface
- All Orpheus functionality accessible via terminal
- Production-ready tool for power users
- Comprehensive error handling and user experience

#### **Phase 2: MCP Integration** (Future)
- Create paired Model Context Protocol (MCP) application
- Bridge CLI functionality with AI/LLM interfaces
- Enable natural language music discovery and management
- Seamless integration between human and AI music workflows

### **Expected User Updates & Iterations**
- **Continuous refinement** based on real-world usage
- **Feature requests** from user experience
- **Bug fixes** and edge case handling
- **Performance optimizations** for large datasets
- **Interface improvements** for better usability

### **CLI Completion Criteria**
- [ ] All major Orpheus features accessible
- [ ] Robust error handling and recovery
- [ ] Comprehensive search and filtering
- [ ] Batch operations and automation support
- [ ] Production-ready stability and performance
- [ ] Complete user documentation

### **MCP Integration Vision**
- Natural language album search: "Find me The Prodigy's best album with good vinyl rips"
- AI-assisted music discovery: "Recommend similar artists to this torrent group"
- Automated collection management: "Download FLAC versions of my favorite albums"
- Intelligent metadata enhancement: "Analyze this artist's discography patterns"

---

## 🔧 Next Steps & Potential Improvements

### Immediate Refinements
- [ ] Fine-tune release grouping algorithm
- [ ] Enhance error handling for edge cases
- [ ] Improve metadata display formatting
- [ ] Add more download options

### Feature Enhancements
- [ ] Batch download capabilities
- [ ] Search history and favorites
- [ ] Release comparison tools
- [ ] Enhanced filtering options

### Technical Improvements
- [ ] Configuration file validation
- [ ] Better credential management
- [ ] Performance optimizations
- [ ] Comprehensive error logging

---

## 🐛 Known Issues & Limitations

### Current Limitations
- Hardcoded credentials in script (security concern)
- Limited error recovery for network issues
- No download progress indication
- Single-threaded torrent downloads

### Edge Cases to Address
- Albums with unusual metadata
- Very large discographies (100+ releases)
- Network timeouts during API calls
- Invalid torrent files



## Newest updates

--

The project status for the Orpheus Collage Tools has been updated to reflect significant enhancements in functionality and user interface design. The latest version of the tool now incorporates a more robust and accurate method for fetching and displaying music releases, addressing previous limitations and improving the overall user experience.

Key improvements have been made to the release filtering and sorting logic. The tool now correctly identifies "official releases" by utilizing the `releaseType` from the Orpheus API, a significant improvement over the previous guesswork-based logic. This ensures that users can reliably filter for official albums, EPs, singles, and other recognized release formats. Furthermore, a sophisticated sorting mechanism has been implemented, prioritizing primary release types such as albums and EPs, and then sorting chronologically by year.

The interactive menu, a core component of the tool, has also seen substantial upgrades. To handle large discographies, the tool now fetches all releases from an artist, not just the first page of results. Additionally, a dynamic filtering system has been introduced, allowing users to further refine the displayed releases by type directly from the interactive menu.

Finally, the command-line interface has been refined for better readability and usability. This includes more compact and organized display of filtering options, the ability to toggle the visibility of track listings to save screen space, and a general improvement in the layout to ensure that the most critical release information is always visible to the user. The terminology within the interface has also been updated for greater clarity, with terms like "albums" being replaced by the more accurate "releases." These updates collectively represent a significant step forward in the capabilities and polish of the Orpheus Collage Tools.

## 📚 Development Context

This project emerged from the need to overcome Orpheus.network API limitations while providing a user-friendly interface for music discovery and downloading. The key insight was switching from format-based to release-based organization, making it much easier to understand what you're actually downloading.

The tool successfully bridges the gap between Orpheus's comprehensive music catalog and practical usability, turning a complex web interface into a streamlined command-line experience.

**Ready for continued development and refinement!** 🚀