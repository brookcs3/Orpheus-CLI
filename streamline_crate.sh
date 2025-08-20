#!/bin/bash

# Update the crate removing the large Smithsonian compilation
echo "📦 Removing large Smithsonian compilation from crate..."

# Update the crate JSON file without the 4.1GB compilation
cat > /Users/cameronbrooks/.orpheus/crates/25_forgotten_female_rap.json << 'EOF'
{
  "name": "25 Forgotten Female Rap Albums (1985-1993)",
  "description": "A curated collection of 8 confirmed rare female rap albums from the golden era (1985-1993). Includes pioneering female MCs who shaped hip-hop but are often overlooked.",
  "created": "2025-01-05",
  "updated": "2025-01-05", 
  "albums": [
    {
      "artist": "Sparky D",
      "album": "This Is Sparky D's World",
      "year": 1988,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "177.4 MB",
      "seeders": 2,
      "notes": "Early battle rapper who answered Roxanne Shanté"
    },
    {
      "artist": "Sparky D", 
      "album": "Fly Girls! (B-Boys Beware: Revenge of the Super Female Rappers!)",
      "year": 2009,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "560.9 MB", 
      "seeders": 4,
      "notes": "★ COMPILATION featuring JJ Fad, Sweet Tee, Cookie Crew, The Sequence, Dimples D"
    },
    {
      "artist": "The Conscious Daughters",
      "album": "Ear To The Street", 
      "year": 1993,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "268.2 MB",
      "seeders": 3,
      "notes": "Oakland duo, political and conscious rap"
    },
    {
      "artist": "BWP",
      "album": "The Bytches",
      "year": 1991,
      "status": "FOUND", 
      "format": "FLAC Lossless",
      "size": "424.1 MB",
      "seeders": 5,
      "notes": "Controversial duo from Queens, hardcore/shock rap"
    },
    {
      "artist": "Boss",
      "album": "Born Gangstaz",
      "year": 1993,
      "status": "FOUND",
      "format": "FLAC Lossless", 
      "size": "276.6 MB",
      "seeders": 1,
      "notes": "Detroit female duo, gangsta rap pioneers for women"
    },
    {
      "artist": "Sweet Tee",
      "album": "It's Tee Time",
      "year": 1988,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "232.3 MB",
      "seeders": 2,
      "notes": "Produced by Hurby Luv Bug, jazz-influenced hip-hop"
    },
    {
      "artist": "Ms. Melodie",
      "album": "Diva", 
      "year": 1989,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "313.1 MB",
      "seeders": 4,
      "notes": "Wife of KRS-One, member of Boogie Down Productions"
    },
    {
      "artist": "Monie Love",
      "album": "Down to Earth",
      "year": 1990,
      "status": "FOUND",
      "format": "FLAC Lossless",
      "size": "283.3 MB",
      "seeders": 7,
      "notes": "British-American rapper, full 13-track album available"
    }
  ],
  "download_summary": {
    "confirmed_albums": 8,
    "total_size_gb": 2.3,
    "average_seeders": 3.5,
    "download_priority": [
      "1. Fly Girls! compilation (560.9 MB) - 6 artists at once!",
      "2. BWP - The Bytches (424.1 MB) - Highest seeders",
      "3. Ms. Melodie - Diva (313.1 MB) - BDP connection", 
      "4. Monie Love - Down to Earth (283.3 MB) - Full album",
      "5. Boss - Born Gangstaz (276.6 MB) - Detroit pioneers",
      "6. Conscious Daughters - Ear To The Street (268.2 MB) - Oakland conscious rap",
      "7. Sweet Tee - It's Tee Time (232.3 MB) - Hurby Luv Bug production",
      "8. Sparky D - This Is Sparky D's World (177.4 MB) - Battle rap classic"
    ]
  },
  "download_commands": [
    "# Use ./collage_tools to download each album:",
    "# 1. Search artist -> 2. Download -> d 1 a1 (for FLAC)",
    "# Start with 'Fly Girls!' - gets you 6 artists from the list!"
  ]
}
EOF

echo "✅ Updated crate - removed 4.1GB Smithsonian compilation"
echo "📊 Final total: 2.3 GB of focused female rap collection"
echo ""
echo "🎯 STREAMLINED DOWNLOAD LIST (8 albums):"
echo "   1. Fly Girls! compilation (560.9 MB) - 6 artists!"
echo "   2. BWP - The Bytches (424.1 MB)"
echo "   3. Ms. Melodie - Diva (313.1 MB)" 
echo "   4. Monie Love - Down to Earth (283.3 MB)"
echo "   5. Boss - Born Gangstaz (276.6 MB)"
echo "   6. Conscious Daughters - Ear To The Street (268.2 MB)"
echo "   7. Sweet Tee - It's Tee Time (232.3 MB)"
echo "   8. Sparky D - This Is Sparky D's World (177.4 MB)"
echo ""
echo "💡 Much more manageable 2.3GB collection!"
