#!/usr/bin/env python3
"""
Search the local collage database and fetch details via API
"""

import json
import asyncio
import argparse
from pathlib import Path
from typing import List, Dict
import aiohttp
import ssl
import os

class CollageSearcher:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or self.get_api_key()
        self.cache_dir = Path.home() / '.orpheus' / 'collage_db'
        self.db_file = self.cache_dir / 'collage_database.json'
        self.database = self.load_database()
        
    def get_api_key(self) -> str:
        """Get API key from config or environment"""
        # Try environment variable
        api_key = os.getenv('ORPHEUS_API_KEY')
        if api_key:
            return api_key
        
        # Try config file
        config_path = Path.home() / '.orpheus' / 'config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                return config.get('api_key', '')
        
        return ''
    
    def load_database(self) -> Dict:
        """Load the local collage database"""
        if not self.db_file.exists():
            print("❌ No collage database found. Run fetch_all_collages.py first!")
            return None
        
        with open(self.db_file, 'r') as f:
            return json.load(f)
    
    def search(self, query: str) -> List[Dict]:
        """Simple text search in collage names"""
        if not self.database:
            return []
        
        query_lower = query.lower()
        results = []
        
        for collage in self.database['collages']:
            if query_lower in collage['name'].lower():
                results.append(collage)
        
        return results
    
    def filter_by_category(self, category: str) -> List[Dict]:
        """Get all collages in a category"""
        if not self.database:
            return []
        
        return self.database['by_category'].get(category, [])
    
    def get_by_id(self, collage_id: int) -> Dict:
        """Get collage by ID"""
        if not self.database:
            return None
        
        return self.database['by_id'].get(str(collage_id))
    
    def list_categories(self) -> List[str]:
        """List all available categories"""
        if not self.database:
            return []
        
        return list(self.database['by_category'].keys())
    
    async def fetch_collage_details(self, collage_id: int):
        """Fetch full collage details from API"""
        if not self.api_key:
            print("❌ No API key found. Set ORPHEUS_API_KEY or update config.json")
            return None
        
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            url = "https://orpheus.network/ajax.php"
            headers = {
                'Authorization': f'token {self.api_key}',
                'User-Agent': 'CollageSearcher/1.0'
            }
            
            params = {
                'action': 'collage',
                'id': collage_id,
                'page': 1
            }
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
        
        return None

async def main():
    parser = argparse.ArgumentParser(description="Search local collage database")
    parser.add_argument('query', nargs='?', help='Search query for collage names')
    parser.add_argument('--category', help='Filter by category')
    parser.add_argument('--list-categories', action='store_true', help='List all categories')
    parser.add_argument('--id', type=int, help='Get specific collage by ID')
    parser.add_argument('--fetch', action='store_true', help='Fetch full details from API for search results')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    searcher = CollageSearcher()
    
    if not searcher.database:
        return
    
    if args.stats:
        print(f"\n📊 Collage Database Statistics")
        print(f"   Total collages: {searcher.database['total']}")
        print(f"   Last updated: {searcher.database['last_updated']}")
        print(f"\n   By category:")
        for category, items in searcher.database['by_category'].items():
            print(f"      {category}: {len(items)} collages")
        return
    
    if args.list_categories:
        print("\n📂 Available categories:")
        for category in sorted(searcher.list_categories()):
            count = len(searcher.database['by_category'][category])
            print(f"   {category}: {count} collages")
        return
    
    if args.id:
        collage = searcher.get_by_id(args.id)
        if collage:
            print(f"\nCollage #{args.id}:")
            print(f"   Name: {collage['name']}")
            print(f"   Category: {collage.get('category', 'Unknown')}")
            print(f"   Torrents: {collage.get('torrent_count', 'Unknown')}")
            
            if args.fetch:
                print("\n📥 Fetching full details from API...")
                details = await searcher.fetch_collage_details(args.id)
                if details:
                    print(f"   Description: {details.get('description_raw', 'None')[:200]}...")
                    print(f"   Total albums: {len(details.get('torrentGroupIDList', []))}")
        else:
            print(f"❌ Collage #{args.id} not found in database")
        return
    
    # Search by query or category
    results = []
    
    if args.category:
        results = searcher.filter_by_category(args.category)
        print(f"\n🔍 Collages in category '{args.category}':")
    elif args.query:
        results = searcher.search(args.query)
        print(f"\n🔍 Search results for '{args.query}':")
    else:
        parser.print_help()
        return
    
    if not results:
        print("   No results found")
        return
    
    # Display results
    for i, collage in enumerate(results[:50], 1):  # Limit to 50 results
        print(f"\n{i:2d}. [{collage['id']}] {collage['name']}")
        print(f"    Category: {collage.get('category', 'Unknown')}")
        if 'torrent_count' in collage:
            print(f"    Torrents: {collage['torrent_count']}")
        if 'creator' in collage:
            print(f"    Creator: {collage['creator']}")
    
    if len(results) > 50:
        print(f"\n... and {len(results) - 50} more results")
    
    # Optionally fetch details for first result
    if args.fetch and results:
        first = results[0]
        print(f"\n📥 Fetching details for: {first['name']}...")
        details = await searcher.fetch_collage_details(first['id'])
        if details:
            print(f"\nDescription: {details.get('description_raw', 'None')[:500]}...")
            print(f"Total albums: {len(details.get('torrentGroupIDList', []))}")

if __name__ == "__main__":
    asyncio.run(main())
