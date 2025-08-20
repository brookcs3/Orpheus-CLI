# Automation Examples

Create custom shell scripts to automate themed music discovery and collection management using the Orpheus CLI tools.

## Creating Themed Music Collections

### Example: Creating a Custom Crate

```bash
#!/bin/bash
# Create a themed crate for specific music collection

echo "📦 Creating crate for My Theme..."

# Create the crate JSON file
# Navigate to project directory first
cd ~/.orpheus
cat > resources/data/crates/my_theme.json << 'EOF'
{
  "name": "My Theme",
  "description": "Custom collection description",
  "albums": []
}
EOF

echo "✅ Crate created! Use: ./collage_tools crate download 'My Theme'"
```

### Example: Batch Album Search

```bash
#!/bin/bash
# Search for multiple albums in a theme

declare -a ALBUMS=(
    "Artist Name|Album Title"
    "Another Artist|Another Album"  
    "Third Artist|Third Album"
)

LOG_FILE="search_results_$(date +%Y%m%d_%H%M%S).log"
echo "Starting batch search..." > "$LOG_FILE"

for album in "${ALBUMS[@]}"; do
    artist=$(echo $album | cut -d'|' -f1)
    title=$(echo $album | cut -d'|' -f2)
    
    echo "🔍 Searching: $artist - $title"
    echo "Searching: $artist - $title" >> "$LOG_FILE"
    
    ./collage_tools find-album --artist "$artist" --album "$title" >> "$LOG_FILE" 2>&1
    
    sleep 2  # Rate limiting
done

echo "✅ Search complete! Check $LOG_FILE"
```

### Example: Themed Collection Discovery

```bash
#!/bin/bash
# Find tracks sampled by a specific artist

echo "🎧 Searching for Tracks Sampled by The Prodigy"
echo "================================================"

# Known samples used by The Prodigy
declare -A samples=(
    ["Breathe"]="Johnny Pate|Shaft in Africa"
    ["Firestarter"]="The Breeders|S.O.S."  
    ["Smack My Bitch Up"]="Ultramagnetic MCs|Give the Drummer Some"
)

for track in "${!samples[@]}"; do
    sample_info="${samples[$track]}"
    artist=$(echo $sample_info | cut -d'|' -f1)
    album=$(echo $sample_info | cut -d'|' -f2)
    
    echo "🎵 $track samples: $artist - $album"
    ./collage_tools find-album --artist "$artist" --album "$album" --show-collages
    echo ""
done
```

### Example: Crate Management Automation

```bash
#!/bin/bash
# Streamline crate operations

CRATE_NAME="$1"

if [ -z "$CRATE_NAME" ]; then
    echo "Usage: $0 <crate_name>"
    exit 1
fi

echo "📦 Managing crate: $CRATE_NAME"

# List current contents
echo "Current contents:"
./collage_tools crate list | grep -A5 "$CRATE_NAME"

# Download with preferred format
echo "🔽 Starting download with FLAC preference..."
./collage_tools crate download "$CRATE_NAME" --prefer-flac

echo "✅ Crate management complete!"
```

## Tips for Automation Scripts

1. **Rate Limiting**: Add `sleep 2` between API calls to avoid rate limits
2. **Logging**: Capture output to log files for review
3. **Error Handling**: Check exit codes and handle failures gracefully
4. **Format Preferences**: Always specify `--prefer-320`, `--prefer-v0`, or `--prefer-flac` for downloads
5. **Crate Organization**: Use descriptive names and descriptions for your themed crates

## Real-World Use Cases

- **Genre Deep Dives**: "25 Forgotten Female Rap Albums (1985-1993)"
- **Sample Hunting**: Find original tracks sampled by favorite artists  
- **Label Exploration**: Download complete catalogs from specific record labels
- **Year-Based Collections**: Albums from specific years or decades
- **Collaborative Filtering**: Use collage membership to discover similar artists

Save these scripts in your own automation directory outside the project to keep your custom workflows organized.