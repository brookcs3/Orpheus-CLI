#!/bin/bash
# Download script for 25 Female Rap Albums (1985-1993)
# Prefers MP3 320 or FLAC (not 24bit)

cd ~/.orpheus

# Create log file
LOG_FILE="female_rap_downloads_$(date +%Y%m%d_%H%M%S).log"
echo "Starting download search for 25 Female Rap Albums (1985-1993)" > "$LOG_FILE"
echo "=============================================" >> "$LOG_FILE"

# Array of albums to search
declare -a ALBUMS=(
    "Sparky D|This Is Sparky D's World"
    "The Sequence|The Sequence Party"
    "Finesse and Synquis|Soul Sisters"
    "Antoinette|Who's The Boss?"
    "Ms. Melodie|Diva"
    "Nikki D|Daddy's Little Girl"
    "Harmony|Let There Be Harmony"
    "Choice|The Big Payback"
    "HWA|Az Much Ass Azz U Want"
    "BWP|The Bytches"
    "Conscious Daughters|Ear to the Street"
    "JJ Fad|Not Just a Fad"
    "Silk Tymes Leather|It Ain't Where Ya From"
    "Tam Tam|Do It To Death"
    "Cookie Crew|Born This Way!"
    "Monie Love|Down to Earth"
    "Oaktown's 357|Wild & Loose"
    "L'Trimm|Grab It!"
    "Sweet Tee|It's Tee Time"
    "Dimples D|Dimples"
    "Tairrie B|The Power of a Woman"
    "Yo! Majesty|Gangsta Goddess"
    "Shelly Thunder|Fresh Out the Pack"
    "Boss|Born Gangstaz"
    "Lin Que|Lin Que's Funky Expedition"
)

# Counter for found albums
FOUND=0
NOT_FOUND=0

echo ""
echo "🎵 Starting search for 25 Female Rap Albums..."
echo ""

# Search for each album
for album_info in "${ALBUMS[@]}"; do
    IFS='|' read -r artist album <<< "$album_info"
    
    echo "🔍 Searching for: $artist - $album"
    echo "Searching for: $artist - $album" >> "$LOG_FILE"
    
    # First try exact album search
    RESULT=$(./collage_tools find-album --artist "$artist" --album "$album" 2>&1)
    
    # Check if found
    if echo "$RESULT" | grep -q "Found 0 release"; then
        # Try just artist search
        echo "   ⚠️  Album not found by name, trying artist search..."
        RESULT=$(./collage_tools find-album --artist "$artist" --limit 20 2>&1)
        
        if echo "$RESULT" | grep -q "Found 0 release"; then
            echo "   ❌ Artist not found: $artist"
            echo "   NOT FOUND: $artist - $album" >> "$LOG_FILE"
            ((NOT_FOUND++))
            echo ""
            continue
        fi
    fi
    
    # Parse results to find suitable format
    echo "$RESULT" | grep -E "(MP3 320|FLAC Lossless)" > /tmp/format_check.txt
    
    if [ -s /tmp/format_check.txt ]; then
        echo "   ✅ Found releases with suitable formats"
        echo "   FOUND: $artist - $album" >> "$LOG_FILE"
        echo "$RESULT" | grep -E "(Group ID:|MP3 320|FLAC Lossless)" >> "$LOG_FILE"
        ((FOUND++))
        
        # Extract Group ID for potential download
        GROUP_ID=$(echo "$RESULT" | grep "Group ID:" | head -1 | awk '{print $3}')
        if [ ! -z "$GROUP_ID" ]; then
            echo "   📀 Group ID: $GROUP_ID"
            echo "   To download manually: ./collage_tools find-album --artist \"$artist\" --album \"$album\" --interactive"
        fi
    else
        echo "   ⚠️  No MP3 320 or FLAC found"
        echo "   NO SUITABLE FORMAT: $artist - $album" >> "$LOG_FILE"
    fi
    
    echo ""
    
    # Small delay to avoid rate limiting
    sleep 2
done

# Summary
echo "============================================="
echo "🎵 SEARCH COMPLETE"
echo "============================================="
echo "✅ Albums found: $FOUND"
echo "❌ Albums not found: $NOT_FOUND"
echo ""
echo "📄 Full log saved to: $LOG_FILE"
echo ""
echo "To download albums interactively, use:"
echo "./collage_tools find-album --artist \"ARTIST_NAME\" --interactive"
echo ""
echo "Then use 'd [album_num] [format]' to download"
echo "Look for formats without '24bit' in the name"

# Also save summary to log
echo "" >> "$LOG_FILE"
echo "SUMMARY: Found $FOUND, Not Found $NOT_FOUND" >> "$LOG_FILE"
