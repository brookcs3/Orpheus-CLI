# Orpheus Collage Tools

Interactive CLI for discovering, browsing, and downloading music releases from Orpheus.network private tracker.

## Quick Start

### 1. Setup Configuration
```bash
# Create your config directory (first time only)
mkdir -p ~/.orpheus-config

# Create your config file with your Orpheus credentials
cat > ~/.orpheus-config/config.json << EOF
{
  "username": "your_orpheus_username",
  "password": "your_orpheus_password", 
  "api_key": "your_orpheus_api_key"
}
EOF

# The project will automatically find your config via symlink
ln -sf ~/.orpheus-config/config.json config.json
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Interactive CLI
```bash
./collage_tools
```

## Features

- **🎤 Artist Search** - Find all releases by artist with smart filtering (Albums, EPs, Singles, etc.)
- **🔍 Collage Discovery** - See which curated collections contain specific albums  
- **📦 Crate System** - Create wishlists and bulk download later
- **⬇️ Bulk Downloads** - Download entire collages with format preferences
- **🎯 Release-Based Organization** - View by actual pressings/labels, not just file formats
- **🎵 Interactive Browsing** - One album per page with complete metadata and navigation

## What Makes This Better Than the Main Site

- **Enhanced filtering** - Show just Beatles singles (impossible on main site)
- **Release-based organization** - See all 23 pressings of "The Fat Of The Land" with different labels/catalog numbers
- **Collage navigation** - Discover music through curated collections with improved interface
- **Wishlist system** - Add albums while browsing, download all at once later
- **Format preferences** - Bulk download with FLAC/320/V0 preferences

## Planned Features

- **🤖 MCP Integration** - Model Context Protocol server for AI assistant interaction
- **🎵 Track Search** - Search by track name with fuzzy matching
- **🔄 Enhanced UI** - Improved visual design and navigation persistence
- **📊 Better Crate Management** - Numbered selection and enhanced browsing

## Directory Structure

```
orpheus-cli/
├── collage_tools           # Main interactive program
├── config.json            # → symlink to ~/.orpheus-config/config.json
├── requirements.txt        # Python dependencies
├── lib/                   # Core functionality
└── resources/            # Additional documentation and future features
    ├── docs/             # Full documentation & automation examples
    ├── mcp/              # MCP server (planned integration)
    └── data/             # User data
        └── crates/       # Your saved wishlists
```

## Documentation

- **Quick Reference**: `resources/docs/quick-reference-card.md`  
- **Full User Guide**: `resources/docs/user-guide.md`
- **Scripting Guide**: `resources/docs/scripting-automation-guide.md`
- **Custom Examples**: `resources/docs/custom-automation-examples.md`
- **Development Guide**: `resources/docs/development-guide.md`

## Download Location

All torrent files are downloaded to:
- **macOS/Windows**: `~/Documents/Orpheus/`
- **Linux**: `~/Documents/Orpheus/`

Individual torrents go directly to this folder, while collage downloads create subfolders like `collage_6936_Sampled_by_The_Prodigy/`.

## Security

Your Orpheus credentials are stored in `~/.orpheus-config/config.json` outside the project directory and will never be committed to git.

## Example Workflow

```bash
# Start interactive mode
./collage_tools

# 1. Search for artist → filter to Albums only → browse releases
# 2. Add interesting albums to a crate while browsing  
# 3. Later: bulk download entire crate with FLAC preference
# 4. Or: discover new music by exploring collages albums belong to
```

This tool transforms the Orpheus experience from tedious web browsing into efficient music discovery.