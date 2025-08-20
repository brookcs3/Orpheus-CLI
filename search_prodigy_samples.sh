#!/bin/bash
# Search for tracks famously sampled by The Prodigy
# Based on documented samples from their biggest hits

echo "🎧 Searching for Tracks Sampled by The Prodigy"
echo "================================================"
echo ""

# Known samples used by The Prodigy
declare -A samples=(
    ["Art of Noise - Close (To The Edit)"]="Sampled in 'Firestarter' (1996)"
    ["The Breeders - S.O.S."]="Sampled in 'Firestarter' (1996)"
    ["Kelly Charles - You're No Good for Me"]="Sampled in 'No Good (Start the Dance)' (1994)"
    ["Nirvana - Very Ape"]="Sampled in 'Voodoo People' (1994)"
    ["Pop Will Eat Itself - Their Law"]="Collaboration on 'Their Law' (1994)"
    ["L7 - Fuel My Fire"]="Covered/sampled in 'Fuel My Fire' (1997)"
    ["The JB's - The Grunt"]="Sampled in 'Poison' (1995)"
    ["Genaside II - Narra Mine"]="Sampled in 'Their Law' (1994)"
    ["Beastie Boys - It's the New Style"]="Sampled in 'Funky Shit' (1996)"
    ["Ultramagnetic MCs - Give the Drummer Some"]="Sampled in 'Smack My Bitch Up' (1997)"
    ["Kool & The Gang - Jungle Boogie"]="Sampled in 'Smack My Bitch Up' (1997)"
    ["Rage Against the Machine - Bulls on Parade"]="Sampled in 'Smack My Bitch Up' (1997)"
)

echo "📋 Famous Prodigy Samples Found on Orpheus:"
echo ""

# Search for each sampled artist
for sample in "${!samples[@]}"; do
    # Extract artist and track from the key
    artist=$(echo "$sample" | cut -d' ' -f1-3 | sed 's/ - .*//')
    track=$(echo "$sample" | sed 's/.* - //')
    
    echo "🔍 $sample"
    echo "   ${samples[$sample]}"
    
    # Search by artist
    result=$(python3 /Users/cameronbrooks/.orpheus/orpheus_cli.py search --artist "$artist" 2>/dev/null | head -15)
    
    if echo "$result" | grep -q "Found 0 results"; then
        # Try searching by album/track name
        result=$(python3 /Users/cameronbrooks/.orpheus/orpheus_cli.py search --album "$track" 2>/dev/null | head -15)
        
        if echo "$result" | grep -q "Found 0 results"; then
            echo "   ❌ Not found on Orpheus"
        else
            echo "$result" | grep -E "^\s*1\.|FLAC|MP3" | head -3 | sed 's/^/   /'
        fi
    else
        echo "$result" | grep -E "^\s*1\.|FLAC|MP3" | head -3 | sed 's/^/   /'
    fi
    echo ""
done

echo "================================================"
echo ""
echo "💡 Additional Known Samples:"
echo ""
echo "• 'Charly' samples: Charly by The Prodigy samples 'Charly Says' PSA"
echo "• 'Out of Space' samples: Max Romeo - 'Chase the Devil'"
echo "• 'Voodoo People' samples: The Very Best of The Jimmy Castor Bunch"
echo "• 'Breathe' samples: Ray Davies dialog from 'The Young Ones'"
echo ""
echo "🎵 To search for more samples, use:"
echo "   ./orpheus search --artist \"Artist Name\""
echo "   ./orpheus search --album \"Track Name\""
