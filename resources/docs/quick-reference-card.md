# Orpheus Collage Tools - Quick Reference Card

## 🚀 Quick Start
```bash
cd ~/.orpheus
./collage_tools              # Interactive mode
./collage_tools find-album --artist "Name" --interactive  # Direct search
```

## 🎯 Interactive Mode Controls
| Key | Action | When Available |
|-----|--------|----------------|
| **n** | Next album | When more albums exist |
| **t** | Toggle tracklist | Always |
| **c** | Toggle collages | When album is in collages |
| **q** | Quit program | Always |
| **h** | Home (main menu) | Always |
| **s 150** | Skip to album #150 | Always |
| **d 1 a2** | Download album 1, format a2 | Always |
| **1-16** | Filter by release type | When filter menu shown |
| **a** | Show all types | When filtered |

## 📝 Common Commands

### Artist Searches
```bash
# Basic search (first 10 results)
./collage_tools find-album --artist "The Prodigy"

# All releases
./collage_tools find-album --artist "The Prodigy" --all

# Official only (no compilations)
./collage_tools find-album --artist "The Prodigy" --official-only

# Interactive browsing
./collage_tools find-album --artist "The Prodigy" --interactive

# With collage info
./collage_tools find-album --artist "The Prodigy" --show-collages
```

### Album Searches
```bash
# Specific album by artist
./collage_tools find-album --artist "Radiohead" --album "OK Computer"

# Any album by name
./collage_tools find-album --album "Dark Side of the Moon"

# Quick collage check
./collage_tools quick-search --artist "The Beatles" --album "Abbey Road"
```

### Downloads
```bash
# From collage (--prefer is required)
./collage_tools download 6936 --prefer-flac
./collage_tools download 6936 --prefer-320
./collage_tools download 6936 --prefer-v0
```

## 🎵 Release Format Codes
```
Release A: 2009 | Label | Catalog | CD
  [a1] FLAC Lossless     # Use 'd 1 a1' to download
  [a2] MP3 320          # Use 'd 1 a2' to download
  [a3] MP3 V0           # Use 'd 1 a3' to download

Release B: 2011 | Label | Catalog | Vinyl  
  [b1] FLAC 24bit       # Use 'd 1 b1' to download
  [b2] FLAC Lossless    # Use 'd 1 b2' to download
```

## 🔍 Filter Types
| Code | Type | Example Count |
|------|------|---------------|
| 1 | Albums | (121) |
| 3 | Soundtracks | (6) |
| 5 | EPs | (9) |
| 6 | Anthologies | (36) |
| 7 | Compilations | (198) |
| 8 | Samplers | (12) |
| 9 | Singles | (91) |
| 11 | Live albums | (4) |
| 13 | Remixes | (32) |
| 14 | Bootlegs | (13) |
| 16 | Mixtapes | (4) |

## 💡 Pro Tips

### For Humans
1. **Large discographies**: Use `s 100` to jump to album #100
2. **Best quality**: Look for highest seeder count + FLAC
3. **Quick navigation**: Press Enter = next album
4. **Finding rare**: Check collage membership with 'c'
5. **Return home**: Press 'h' anytime to go back to main menu

### For AI/Scripts
1. **Parse carefully**: Group IDs are after "Group ID:"
2. **Exit codes**: 0=success, 1=error, 2=returned to menu
3. **Batch operations**: Use `--all` then parse output
4. **Format preference**: Always use `--prefer-*` for downloads
5. **Avoid rate limits**: Add delays between requests

## 📊 Output Format Examples

### Search Result
```
1. Artist - Album Title
   Group ID: 12345
   📅 Year: 2009
   💿 Available Releases (3):
```

### Download Command
```
d [album_number] [format_code]
d 1 a2  # Download album 1, format a2 (Release A, format 2)
d 3 b1  # Download album 3, format b1 (Release B, format 1)
```

### Skip Command
```
s [page_number]
s 50   # Go to album #50
s 150  # Go to album #150
```

## ⚡ One-Liners

```bash
# Count artist's total releases
./collage_tools find-album --artist "Madonna" --all | grep "total releases" | awk '{print $3}'

# Get all album names for artist
./collage_tools find-album --artist "The Beatles" --all | grep -E "^\d+\." | sed 's/^[0-9]*\. //'

# Check if album is in collages
./collage_tools find-album --artist "Pink Floyd" --album "The Wall" --show-collages | grep -c "collage(s):"

# Interactive search with filters
echo -e "1\nThe Prodigy\n2\nn\nn\nq" | ./collage_tools
```

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Login failed | Check credentials in config.json |
| No results | Try simpler search terms |
| Can't download | Verify format exists (check [a1], [b2] etc.) |
| Timeout | Orpheus may be slow, try again |
| SSL error | Normal for private trackers |

## 📁 File Locations
- Main script: `~/.orpheus/collage_tools`
- Config: `~/.orpheus/config.json`
- Downloads: `~/Downloads/`
- Python scripts: `~/.orpheus/*.py`
