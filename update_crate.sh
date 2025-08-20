#!/bin/bash

# Update the crate with the new Monie Love finding
echo "📦 Updating Female Rap Crate with new discovery..."

# Update the crate JSON file
cat > /Users/cameronbrooks/.orpheus/crates/25_forgotten_female_rap.json << 'EOF'
{
  "name": "25 Forgotten Female Rap Albums (1985-1993)",
  "description": "A collection of 25 forgotten female rap albums from the golden era (1985-1993). Includes pioneering female MCs who shaped hip-hop but are often overlooked.",
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
      "notes": "★ NEW FIND! British-American rapper, full album available"
    }
  ],
  "bonus_compilation": {
    "title": "Smithsonian Anthology of Hip-Hop and Rap", 
    "year": 2021,
    "size": "4.1 GB FLAC", 
    "seeders": 41,
    "relevant_tracks": [
      "The Sequence - Funk You Up",
      "Queen Latifah Feat. Monie Love - Ladies First"
    ],
    "notes": "Massive 129-track compilation with early female rap classics"
  },
  "download_summary": {
    "confirmed_albums": 8,
    "total_size_gb": 2.3,
    "average_seeders": 3.5,
    "priority_order": [
      "1. Fly Girls! compilation (6 artists at once)",
      "2. Smithsonian Anthology (Sequence + more classics)", 
      "3. Monie Love - Down to Earth (283.3 MB)",
      "4. BWP - The Bytches (424.1 MB)",
      "5. Ms. Melodie - Diva (313.1 MB)",
      "6. Boss - Born Gangstaz (276.6 MB)",
      "7. Conscious Daughters - Ear To The Street (268.2 MB)",
      "8. Sweet Tee - It's Tee Time (232.3 MB)",
      "9. Sparky D - This Is Sparky D's World (177.4 MB)"
    ]
  }
}
EOF

echo "✅ Updated crate with 8 confirmed albums + 2 bonus compilations"
echo "📊 New total: ~2.3 GB of rare female rap in FLAC format"
echo ""
echo "🆕 LATEST DISCOVERY:"
echo "   • Monie Love - Down to Earth (1990) - 283.3 MB FLAC - 7 seeders"
echo "   • Full 13-track album available!"
echo ""
echo "🎯 UPDATED DOWNLOAD PRIORITY:"
echo "   1. Fly Girls! compilation (560.9 MB) - Gets you 6 artists!"
echo "   2. Smithsonian Anthology (4.1 GB) - Early classics collection"
echo "   3. Monie Love - Down to Earth (283.3 MB) - Full album"
echo "   4. Individual albums by BWP, Ms. Melodie, Boss, etc."
