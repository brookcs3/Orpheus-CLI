#!/bin/bash

# Download script for the 25 Forgotten Female Rap Albums
echo "🎵 Downloading Female Rap Albums from Crate..."
echo "=============================================="

# Array of download commands for interactive mode
declare -a downloads=(
    "1\nSparky D\n2\nFly Girls\nd 1 a1"
    "1\nSparky D\n2\nThis Is Sparky\nd 1 a1" 
    "1\nConscious Daughters\n2\nEar to the Street\nd 1 a1"
    "1\nBWP\n2\nThe Bytches\nd 1 a1"
    "1\nBoss\n2\nBorn Gangstaz\nd 1 a1"
    "1\nSweet Tee\n2\nIt's Tee Time\nd 1 a1"
    "1\nMs. Melodie\n2\nDiva\nd 1 a1"
)

echo "📋 Ready to download 7 albums in FLAC format:"
echo ""
echo "   1. Fly Girls! compilation (Contains 6 artists from your list!)"
echo "   2. Sparky D - This Is Sparky D's World" 
echo "   3. Conscious Daughters - Ear To The Street"
echo "   4. BWP - The Bytches"
echo "   5. Boss - Born Gangstaz" 
echo "   6. Sweet Tee - It's Tee Time"
echo "   7. Ms. Melodie - Diva"
echo ""
echo "💡 Manual Download Instructions:"
echo "   Run: ./collage_tools"
echo "   Then for each album:"
echo "   - Choose option 1 (Find album)"
echo "   - Enter artist name"
echo "   - Choose option 2 (Download)" 
echo "   - Enter album name"
echo "   - Type 'd 1 a1' to download FLAC version"
echo "   - Type 'q' to quit"
echo ""
echo "🎯 Priority: Start with 'Fly Girls!' compilation - it gets you 6 artists at once!"
