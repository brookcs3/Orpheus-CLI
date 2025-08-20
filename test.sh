#!/bin/bash
echo "🧪 Testing Orpheus CLI..."
echo ""
echo "Testing search (should show results):"
python3 /Users/cameronbrooks/.orpheus/orpheus_cli.py search --artist "Aphex Twin" | head -20
echo ""
echo "✅ If you see search results above, everything is working!"
echo ""
echo "Usage examples:"
echo "  ./orpheus search --artist \"Salt-N-Pepa\""
echo "  ./orpheus search --artist \"MC Lyte\" --format \"FLAC\""
echo "  ./orpheus collage 12345"
echo "  ./orpheus download 123456 789012 --script"
