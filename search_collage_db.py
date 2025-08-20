#!/usr/bin/env python3
"""
Search the complete collage database by artist or album
Find which collages contain specific artists or albums
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict

class CollageSearcher:
    def __init__(self):
        self.cache_dir = Path.home() / '.orpheus' / 'collage_database'
        self.db_file = self.cache_dir / 'complete_collage_database.json'
        self.database = self.load_database()
    
    def load_database(self) -> Dict:
        """Load the complete collage database"""
        if not self.db_file.exists():
            print("❌ No database found. Run build_collage_database.py first!")
            return None
        
        print("📂 Loading database...")
        with open(self.db_file, 'r') as f:
            return json.load(f)
    
    def search_by_artist(self, artist_name: str) -> List[int]:
        """Find collages containing an artist"""
        if not self.database:
            return []
        
        artist_lower = artist_name.lower()
        
        # Exact match
        if artist_lower in self.database['artist_to_collages']:
            return self.database['artist_to_collages'][artist_lower]
        
        # Partial match
        matches = []
        for artist, collage_ids in self.database['artist_to_collages'].items():
            if artist_lower in artist or artist in artist_lower:
                matches.extend(collage_ids)
        
        return list(set(matches))  # Remove duplicates
    
    def search_by_album(self, album_name: str) -> List[int]:
        """Find collages containing an album"""
        if not self.database:
            return []
        
        album_lower = album_name.lower()
        
        # Exact match
        if album_lower in self.database['album_to_collages']:
            return self.database['album_to_collages'][album_lower]
        
        # Partial match
        matches = []
        for album, collage_ids in self.database['album_to_collages'].items():
            if album_lower in album or album in album_lower:
                matches.extend(collage_ids)
        
        return list(set(matches))
    
    def get_collage_info(self, collage_id: int) -> Dict:
        """Get info about a specific collage"""
        if not self.database:
            return None
        
        return self.database['collages'].get(collage_id)
    
    def display_results(self, collage_ids: List[int], search_term: str, search_type: str):
        """Display search results"""
        if not collage_ids:
            print(f"\n❌ No collages found containing {search_type}: '{search_term}'")
            return
        
        print(f"\n✅ Found {len(collage_ids)} collage(s) containing {search_type}: '{search_term}'")
        print("=" * 60)
        
        for i, collage_id in enumerate(collage_ids[:50], 1):  # Limit to 50 results
            collage = self.get_collage_info(collage_id)
            if collage:
                print(f"\n{i}. Collage #{collage_id}: {collage['name']}")
                print(f"   Albums in collage: {len(collage['albums'])}")
                print(f"   URL: https://orpheus.network/collages.php?id={collage_id}")
                
                # Show which albums by this artist are in the collage (if searching by artist)
                if search_type == "artist":
                    artist_lower = search_term.lower()
                    matching_albums = [
                        album for album in collage['albums']
                        if artist_lower in album['artist'].lower()
                    ]
                    if matching_albums:
                        print(f"   Albums by {search_term} in this collage:")
                        for album in matching_albums[:5]:  # Show first 5
                            print(f"      - {album['album_name']} ({album['year']})")
                        if len(matching_albums) > 5:
                            print(f"      ... and {len(matching_albums) - 5} more")
        
        if len(collage_ids) > 50:
            print(f"\n... and {len(collage_ids) - 50} more collages")

def main():
    parser = argparse.ArgumentParser(description="Search collage database by artist or album")
    parser.add_argument('--artist', help='Search by artist name')
    parser.add_argument('--album', help='Search by album name')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    if not args.artist and not args.album and not args.stats:
        parser.print_help()
        return
    
    searcher = CollageSearcher()
    
    if not searcher.database:
        return
    
    if args.stats:
        print("\n📊 Database Statistics:")
        print(f"   Total collages: {searcher.database['stats']['total_collages']}")
        print(f"   Unique artists indexed: {searcher.database['stats']['total_artists']}")
        print(f"   Unique albums indexed: {searcher.database['stats']['total_albums']}")
        print(f"   Last updated: {searcher.database['last_updated']}")
        return
    
    if args.artist:
        collage_ids = searcher.search_by_artist(args.artist)
        searcher.display_results(collage_ids, args.artist, "artist")
    
    if args.album:
        collage_ids = searcher.search_by_album(args.album)
        searcher.display_results(collage_ids, args.album, "album")

if __name__ == "__main__":
    main()
