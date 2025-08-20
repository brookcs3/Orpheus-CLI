#!/bin/bash

# Create a crate for 25 Forgotten Female Rap Albums
echo "📦 Creating crate for 25 Forgotten Female Rap Albums..."

# Create crates directory if it doesn't exist
mkdir -p /Users/cameronbrooks/.orpheus/crates

# Create the crate JSON file
cat > /Users/cameronbrooks/.orpheus/crates/25_forgotten_female_rap.json << 'EOF'
{
  "name": "25 Forgotten Female Rap Albums (1985-1993)",
  "description": "A collection of 25 forgotten female rap albums from the golden era (1985-1993). Includes pioneering female MCs who shaped hip-hop but are often overlooked.",
  "created": "2025-01-05",
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
      "notes": "Compilation featuring JJ Fad, Sweet Tee, Cookie Crew, The Sequence, Dimples D"
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
      "artist": "The Sequence",
      "album": "The Sequence Party",
      "year": 1985,
      "status": "NOT_FOUND",
      "notes": "First all-female rap group to get a record deal, pre-dated Salt-N-Pepa"
    },
    {
      "artist": "Finesse and Synquis",
      "album": "Soul Sisters",
      "year": 1989,
      "status": "NOT_SEARCHED",
      "notes": "Produced by Full Force, great harmonies mixed with rap"
    },
    {
      "artist": "Antoinette",
      "album": "Who's The Boss?",
      "year": 1989,
      "status": "NOT_FOUND",
      "notes": "Hardcore female MC who battled MC Lyte on wax"
    },
    {
      "artist": "Nikki D",
      "album": "Daddy's Little Girl",
      "year": 1991,
      "status": "NOT_SEARCHED",
      "notes": "Def Jam artist produced by Sam Sever and Prince Paul"
    },
    {
      "artist": "Harmony",
      "album": "Let There Be Harmony",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "Produced by Hurby Luv Bug, smooth conscious rap"
    },
    {
      "artist": "Choice",
      "album": "The Big Payback",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "Texas female rapper, one of the first from the South"
    },
    {
      "artist": "HWA",
      "album": "Az Much Ass Azz U Want",
      "year": 1990,
      "status": "NOT_FOUND",
      "notes": "Female response to N.W.A from LA"
    },
    {
      "artist": "JJ Fad",
      "album": "Not Just a Fad",
      "year": 1990,
      "status": "NOT_FOUND",
      "notes": "Follow-up to Supersonic, produced by Arabian Prince"
    },
    {
      "artist": "Silk Tymes Leather",
      "album": "It Ain't Where Ya From",
      "year": 1991,
      "status": "NOT_SEARCHED",
      "notes": "Produced by Naughty by Nature, from LA"
    },
    {
      "artist": "Cookie Crew",
      "album": "Born This Way!",
      "year": 1989,
      "status": "NOT_SEARCHED",
      "notes": "British female rap duo, worked with Beatmasters"
    },
    {
      "artist": "Monie Love",
      "album": "Down to Earth",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "British-American rapper, more underground than hit singles suggest"
    },
    {
      "artist": "Oaktown's 357",
      "album": "Wild & Loose",
      "year": 1989,
      "status": "NOT_SEARCHED",
      "notes": "MC Hammer's female group, but had their own identity"
    },
    {
      "artist": "L'Trimm",
      "album": "Grab It!",
      "year": 1988,
      "status": "NOT_SEARCHED",
      "notes": "Miami bass female duo, known for 'Cars with the Boom'"
    },
    {
      "artist": "Dimples D",
      "album": "Dimples",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "'Sucker DJ' was huge underground, overlooked album"
    },
    {
      "artist": "Tairrie B",
      "album": "The Power of a Woman",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "White female hardcore rapper from LA, rock-influenced"
    },
    {
      "artist": "Lin Que",
      "album": "Lin Que's Funky Expedition",
      "year": 1990,
      "status": "NOT_SEARCHED",
      "notes": "Produced by Mantronix, futuristic sound"
    }
  ],
  "download_commands": [
    "# Download the found albums using these commands:",
    "./collage_tools # Then navigate to download these releases:",
    "# 1. Sparky D - This Is Sparky D's World [a1] FLAC",
    "# 2. Sparky D - Fly Girls! [a1] FLAC (Contains multiple artists)",
    "# 3. Conscious Daughters - Ear To The Street [a1] FLAC", 
    "# 4. BWP - The Bytches [a1] FLAC",
    "# 5. Boss - Born Gangstaz [a1] FLAC",
    "# 6. Sweet Tee - It's Tee Time [a1] FLAC",
    "# 7. Ms. Melodie - Diva [a1] FLAC"
  ]
}
EOF

echo "✅ Created crate: 25_forgotten_female_rap.json"
echo "📋 Crate contains 7 confirmed available albums in FLAC format"
echo ""
echo "🎯 PRIORITY DOWNLOADS (All FLAC):"
echo "   1. Fly Girls! compilation (560.9 MB) - Contains JJ Fad, Sweet Tee, Cookie Crew, Sequence, Sparky D, Dimples D"
echo "   2. Sparky D - This Is Sparky D's World (177.4 MB)"
echo "   3. Conscious Daughters - Ear To The Street (268.2 MB)"
echo "   4. BWP - The Bytches (424.1 MB)" 
echo "   5. Boss - Born Gangstaz (276.6 MB)"
echo "   6. Sweet Tee - It's Tee Time (232.3 MB)"
echo "   7. Ms. Melodie - Diva (313.1 MB)"
echo ""
echo "📁 Total size: ~2.05 GB"
echo "🎵 To download: Use ./collage_tools in interactive mode"
