# Orpheus Collage Tools - AI/Automation Reference

Quick reference for using Orpheus Collage Tools in scripts, automation, or AI assistants.

## Single Command Examples

### Basic Artist Searches
```bash
# Get first 10 albums by artist (default)
./collage_tools find-album --artist "The Prodigy"

# Get ALL albums by artist
./collage_tools find-album --artist "The Prodigy" --all

# Get only official releases (no compilations)
./collage_tools find-album --artist "The Prodigy" --official-only

# Get first 50 results
./collage_tools find-album --artist "The Prodigy" --limit 50

# Interactive browsing (one album per page)
./collage_tools find-album --artist "The Prodigy" --interactive
```

### Album-Specific Searches
```bash
# Search for specific album by artist
./collage_tools find-album --artist "Radiohead" --album "OK Computer"

# Search for album by name only (any artist)
./collage_tools find-album --album "Dark Side of the Moon"

# Find album and show which collages it's in
./collage_tools find-album --artist "Portishead" --album "Dummy" --show-collages
```

### Combined Options
```bash
# Official releases only, with collages, interactive mode
./collage_tools find-album --artist "Radiohead" --official-only --show-collages --interactive

# All releases by artist with collage info
./collage_tools find-album --artist "Madonna" --all --show-collages

# Quick collage search
./collage_tools quick-search --artist "The Beatles" --album "Abbey Road"
```

### Downloading from Collages
```bash
# Download with MP3 320 preference
./collage_tools download 6936 --prefer-320

# Download with FLAC preference
./collage_tools download 6936 --prefer-flac

# Download with MP3 V0 preference
./collage_tools download 6936 --prefer-v0
```

## Exit Codes
- `0` - Success
- `1` - Error (login failed, no results, etc.)
- `2` - User returned to main menu (interactive mode)

## Parsing Output

### Non-Interactive Mode Output Format
```
🔐 Logging in to Orpheus...

🔍 Searching for all releases by The Prodigy...

📊 Sorting 87 releases...
📋 Found 87 total releases

✅ Found 87 release(s)

1. The Prodigy - Invaders Must Die
   Group ID: 12345
   📅 Year: 2009
   💿 Available Releases (3):
   
      Release A: 2009 | Take Me to the Hospital | HOSPCDS01 | CD
        [a1] FLAC Lossless | 445.2 MB | 23 seeders
        [a2] MP3 320 | 163.8 MB | 8 seeders
```

### Key Information to Extract
- Artist name: After "Searching for all releases by"
- Total releases: Number after "Found X total releases"
- Album details: Artist - Album on numbered lines
- Group ID: For API calls
- Release formats: Letters (A, B, C) indicate different releases
- Format codes: [a1], [b2] etc. for download commands

## Automation Examples

### Bash Script - Download Artist's Discography
```bash
#!/bin/bash
ARTIST="The Prodigy"

# Get all albums
./collage_tools find-album --artist "$ARTIST" --all > albums.txt

# Extract group IDs and download FLAC versions
grep "Group ID:" albums.txt | awk '{print $3}' | while read id; do
    echo "Processing album ID: $id"
    # Additional API calls could go here
done
```

### Python Integration
```python
import subprocess
import re

# Search for artist
result = subprocess.run(
    ['./collage_tools', 'find-album', '--artist', 'Radiohead', '--limit', '20'],
    capture_output=True,
    text=True
)

# Parse output
albums = re.findall(r'(\d+)\. (.+) - (.+)', result.stdout)
for num, artist, album in albums:
    print(f"Found: {artist} - {album}")
```

### One-Liner Examples
```bash
# Count total releases for an artist
./collage_tools find-album --artist "Madonna" --all | grep "Found.*total releases" | awk '{print $3}'

# Get all album names
./collage_tools find-album --artist "The Beatles" --all | grep -E "^\d+\." | cut -d'-' -f2-

# Check if album exists in any collage
./collage_tools quick-search --artist "Pink Floyd" --album "The Wall" | grep -c "In.*collage"
```

## Interactive Mode Automation

### Using expect or similar tools
```bash
#!/usr/bin/expect
spawn ./collage_tools
expect "Choose option"
send "1\r"
expect "Enter artist name:"
send "The Prodigy\r"
expect "Choose option"
send "2\r"
# Continue interaction...
```

### Piping commands
```bash
# Navigate to page 50 and quit
echo -e "1\nThe Prodigy\n1\ns 50\nq" | ./collage_tools

# Download specific release
echo -e "1\nRadiohead\n2\nd 1 a1\nq" | ./collage_tools
```

## Common Use Cases

### 1. Check Latest Releases
```bash
./collage_tools find-album --artist "Artist Name" --limit 5
```

### 2. Find Best Quality Version
```bash
# Search and look for highest seeder FLAC
./collage_tools find-album --artist "Artist" --album "Album" --interactive
```

### 3. Catalog Collage Contents
```bash
# For each collage ID
./collage_tools download COLLAGE_ID --prefer-flac --dry-run
```

### 4. Verify Album Exists
```bash
if ./collage_tools find-album --artist "Artist" --album "Album" | grep -q "Found 0 release"; then
    echo "Album not found"
else
    echo "Album exists"
fi
```

## API Integration Notes

- Rate limiting: Add delays between requests
- Authentication: Store credentials securely
- Error handling: Check exit codes
- Parsing: Use structured output parsing, not screen scraping when possible

## Performance Tips

1. Use `--limit` to reduce processing time
2. Add `--official-only` to skip compilations
3. Cache results when doing multiple searches
4. Use specific searches over broad ones
5. Implement exponential backoff for retries

## Debugging

### Verbose Output
```bash
# See what's happening
bash -x ./collage_tools find-album --artist "Test"
```

### Direct Python Execution
```bash
# Bypass bash wrapper for debugging
python3 ~/.orpheus/find_album_collages.py --artist "Test" --interactive
```

### Common Issues
- Exit code 1: Usually authentication or network issues
- Empty results: Check artist spelling, try without special characters
- Timeout: Orpheus might be slow, increase timeout values
