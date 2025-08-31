# Orpheus Collage Tools

[![PyPI version](https://badge.fury.io/py/orpheus-collage-tools.svg)](https://pypi.org/project/orpheus-collage-tools/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A cross-platform command-line tool for discovering, browsing, and downloading music releases from Orpheus.network private tracker.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Platform-Specific Notes](#platform-specific-notes)
- [Features](#features)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Development](#development)

## Installation

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: macOS, Windows, or Linux
- **Internet Connection**: Required for API access

### Install from PyPI

The easiest way to install Orpheus Collage Tools is via pip:

```bash
pip install orpheus-collage-tools
```

### Verify Installation

After installation, verify it works:

```bash
orpheus --help
```

You should see the help message with available commands.

## Quick Start

### 1. First Run Setup

Run the tool for the first time to set up your configuration:

```bash
orpheus
```

This will:

- Create a configuration directory
- Prompt for your Orpheus credentials
- Validate your API access
- Save secure configuration

### 2. Interactive Mode

Start the interactive menu system:

```bash
orpheus
```

### 3. Command Line Usage

Use specific commands directly:

```bash
# Search for artist releases
orpheus find-album --artist "The Prodigy" --interactive

# Download torrents from a collage
orpheus download 6936 --prefer-flac

# Manage crates
orpheus crate list
```

## Configuration

### Automatic Setup

On first run, the tool automatically creates configuration files:

- **macOS**: `~/.orpheus/config.json`
- **Windows**: `%APPDATA%/orpheus/config.json`
- **Linux**: `~/.orpheus/config.json`

### Manual Configuration

You can also create the configuration file manually:

```bash
# Create config directory
mkdir -p ~/.orpheus  # Linux/macOS
# or
mkdir %APPDATA%/orpheus  # Windows

# Create config file
cat > ~/.orpheus/config.json << EOF
{
  "username": "your_orpheus_username",
  "password": "your_orpheus_password",
  "api_key": "your_orpheus_api_key"
}
EOF
```

### Getting Your API Key

1. Go to [Orpheus User Settings](https://orpheus.network/user.php?action=edit&id=8956#access)
2. Scroll down to the "Access" section
3. Copy your API key

### Security Notes

- Configuration files are created with owner-only permissions (600)
- Credentials are never logged or stored in plain text outside the config file
- The tool validates credentials before saving

## Usage

### Interactive Mode

The interactive mode provides a guided menu system:

```bash
orpheus
```

Available options:

1. **Find artist albums & releases** - Browse artist discographies
2. **Find collages** - Discover curated collections
3. **Download torrents** - Download from specific collages
4. **Manage crates** - Create and manage wishlists
5. **Load crate and browse** - Use saved collections
6. **Exit**

### Command Line Interface

#### Artist Search

```bash
# Interactive search with full results
orpheus find-album --artist "The Beatles" --interactive

# Search for specific album
orpheus find-album --artist "The Beatles" --album "Abbey Road"

# Official releases only
orpheus find-album --artist "The Beatles" --official-only
```

#### Collage Operations

```bash
# Find collages featuring an artist
orpheus find-artist-collages "Radiohead"

# Download torrents from collage (REQUIRED: --prefer option)
orpheus download 6936 --prefer-320    # MP3 320 CBR
orpheus download 6936 --prefer-v0     # MP3 V0 VBR
orpheus download 6936 --prefer-flac   # FLAC Lossless
```

#### Crate Management

```bash
# List all crates
orpheus crate list

# Create new crate
orpheus crate create "My Favorites"

# Download crate contents
orpheus crate download "My Favorites"
```

### Download Locations

Torrents are saved to:

- **macOS**: `~/Documents/Orpheus/`
- **Windows**: `~/Documents/Orpheus/`
- **Linux**: `~/Documents/Orpheus/`

Collage downloads create subfolders like:

```
~/Documents/Orpheus/collage_6936_Sampled_by_The_Prodigy/
```

## Platform-Specific Notes

### macOS

- Uses optimized bash script for best performance
- Full interactive features supported
- Native macOS file permissions
- Configuration stored in `~/.orpheus/`

### Windows

- Uses Python implementation with batch file launcher
- Full feature parity with other platforms
- Configuration stored in `%APPDATA%/orpheus/`
- Compatible with Windows 10/11

### Linux

- Uses Python implementation
- Full feature parity
- Configuration stored in `~/.orpheus/`
- Compatible with all major distributions

### Platform Detection

The tool automatically detects your operating system and uses the appropriate implementation:

- **macOS**: Bash script execution
- **Windows/Linux**: Python implementation

## Features

### 🎤 Artist Discovery

- Browse complete artist discographies
- Filter by release type (Albums, EPs, Singles)
- Official vs. unofficial releases
- Interactive browsing with pagination

### 🔍 Collage Exploration

- Find collages containing specific artists
- Discover music through curated collections
- Search collages by name or keywords
- Browse collage contents before downloading

### 📦 Crate System

- Create wishlists while browsing
- Save albums for later download
- Bulk download entire collections
- Organize music discovery workflow

### ⬇️ Smart Downloads

- Multiple format options (320, V0, FLAC)
- Automatic format preference handling
- Batch download from collages
- Progress tracking and error handling

### 🎵 Enhanced Interface

- Interactive menu system
- Color-coded output
- Clear navigation and help
- Cross-platform compatibility

## Examples

### Complete Workflow

```bash
# 1. Install the package
pip install orpheus-collage-tools

# 2. First run setup
orpheus

# 3. Search for an artist
orpheus find-album --artist "Pink Floyd" --interactive

# 4. Create a crate for favorites
orpheus crate create "Classic Rock"

# 5. Download a collage
orpheus download 12345 --prefer-flac

# 6. List your crates
orpheus crate list
```

### Advanced Usage

```bash
# Search for specific album across all collages
orpheus find-album --artist "Radiohead" --album "OK Computer"

# Find all collages featuring an artist
orpheus find-artist-collages "Bjork"

# Download with specific format preference
orpheus download 67890 --prefer-320

# Manage multiple crates
orpheus crate create "Electronic"
orpheus crate create "Jazz"
orpheus crate list
```

## Troubleshooting

### Common Issues

#### "Command not found" Error

```bash
# Make sure the package is installed
pip install orpheus-collage-tools

# Check if it's in your PATH
which orpheus

# Try running with python -m
python -m orpheus_collage_tools.cli
```

#### Configuration Issues

```bash
# Delete and recreate config
rm ~/.orpheus/config.json
orpheus  # Run setup again
```

#### Permission Errors

```bash
# Fix config file permissions
chmod 600 ~/.orpheus/config.json
```

#### Download Issues

- Ensure you have write permissions to `~/Documents/Orpheus/`
- Check your internet connection
- Verify your Orpheus credentials are correct

### Getting Help

```bash
# Show all available commands
orpheus --help

# Run in interactive mode for guided help
orpheus
```

### Debug Mode

For troubleshooting, you can run individual Python scripts:

```bash
# Test artist search directly
python -c "from orpheus_collage_tools.lib.find_album_collages import main; main()"

# Check configuration
python -c "from orpheus_collage_tools.core import OrpheusTools; print(OrpheusTools().load_config())"
```

## Security

### Credential Storage

- API keys and passwords are stored locally only
- Configuration files use secure permissions (600)
- No data is transmitted except to Orpheus.network
- Credentials are validated before storage

### Network Security

- All communication uses HTTPS
- API keys are sent in Authorization headers
- No sensitive data is logged
- Cookies are handled securely

### Best Practices

- Keep your API key private
- Don't share your configuration files
- Use strong, unique passwords
- Regularly update your credentials if needed

## Development

### Source Code

The source code is available on GitHub:

- Repository: [https://github.com/brookcs3/Orpheus-CLI](https://github.com/brookcs3/Orpheus-CLI)
- Issues: [https://github.com/brookcs3/Orpheus-CLI/issues](https://github.com/brookcs3/Orpheus-CLI/issues)

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Building from Source

```bash
# Clone the repository
git clone https://github.com/cameronbrooks/orpheus-collage-tools.git
cd orpheus-collage-tools

# Install in development mode
pip install -e .

# Run tests
python -m pytest
```

### Requirements

- Python 3.8+
- aiohttp>=3.8.0
- beautifulsoup4>=4.11.0
- requests>=2.28.0

## License

MIT License - see LICENSE file for details.

## Support

For issues, questions, or feature requests:

- GitHub Issues: [https://github.com/cameronbrooks/orpheus-collage-tools/issues](https://github.com/cameronbrooks/orpheus-collage-tools/issues)
- PyPI Page: [https://pypi.org/project/orpheus-collage-tools/](https://pypi.org/project/orpheus-collage-tools/)

## Changelog

### Version 1.0.0

- Initial release
- Cross-platform support (macOS, Windows, Linux)
- Interactive menu system
- Artist and collage search
- Bulk download functionality
- Crate management system
- Secure configuration handling
- PyPI package distribution

---

**Happy music discovering!** 🎵✨
