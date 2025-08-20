#!/usr/bin/env python3
"""
Build a complete searchable database of all Orpheus collages
Allows searching by artist or album to find containing collages
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
import aiohttp
import ssl
from bs4 import BeautifulSoup
from typing import Dict, List, Set
import time

class OrpheusCollageDatabase:
    def __init__(self, username: str, password: str, api_key: str):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.base_url = "https://orpheus.network"
        self.session = None
        self.cache_dir = Path.home() / '.orpheus' / 'collage_database'
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        
    async def __aenter__(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def login(self) -> bool:
        """Login to Orpheus website"""
        login_url = f"{self.base_url}/login.php"
        
        login_data = {
            'username': self.username,
            'password': self.password,
            'keeplogged': '1',
            'login': 'Log in'
        }
        
        async with self.session.post(login_url, data=login_data, allow_redirects=False) as response:
            if 'session' in response.cookies or response.status in [302, 303]:
                async with self.session.get(f"{self.base_url}/index.php") as index_response:
                    text = await index_response.text()
                    if 'logout.php' in text:
                        print("✅ Successfully logged in to Orpheus")
                        return True
        
        print("❌ Login failed")
        return False
    
    async def fetch_all_collage_ids(self) -> List[Dict]:
        """Fetch all collage IDs and names from website"""
        all_collages = []
        page = 1
        
        print("\n📥 Step 1: Getting all collage IDs from website...")
        
        while True:
            url = f"{self.base_url}/collages.php"
            params = {'page': page}
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    break
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                found_any = False
                for link in soup.find_all('a', href=re.compile(r'collages\.php\?id=\d+')):
                    collage_id = re.search(r'id=(\d+)', link['href'])
                    if collage_id:
                        found_any = True
                        collage_info = {
                            'id': int(collage_id.group(1)),
                            'name': link.get_text(strip=True)
                        }
                        if collage_info['id'] not in [c['id'] for c in all_collages]:
                            all_collages.append(collage_info)
                
                if not found_any:
                    break
                
                print(f"   Page {page}: {len(all_collages)} collages found...")
                
                has_next = bool(soup.find('a', string=re.compile(r'Next')))
                if not has_next:
                    break
                
                page += 1
                await asyncio.sleep(0.5)
        
        print(f"   Total: {len(all_collages)} collages\n")
        return all_collages
    
    async def fetch_collage_contents(self, collage_id: int) -> Dict:
        """Fetch complete contents of a collage via API"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'CollageDB/1.0'
        }
        
        all_albums = []
        page = 1
        collage_info = {'id': collage_id}
        
        while True:
            params = {
                'action': 'collage',
                'id': collage_id,
                'page': page
            }
            
            try:
                async with self.session.get(url, params=params, headers=headers) as response:
                    if response.status != 200:
                        break
                    
                    data = await response.json()
                    if data.get('status') != 'success':
                        break
                    
                    resp = data['response']
                    
                    # First page - get collage info
                    if page == 1:
                        collage_info['name'] = resp.get('name', '')
                        collage_info['total'] = len(resp.get('torrentGroupIDList', []))
                    
                    # Get album/artist info from this page
                    for item in resp.get('torrentgroups', []):
                        # The actual group info is nested inside 'group'
                        group = item.get('group', {})
                        
                        # Extract artist names from musicInfo
                        artists = []
                        music_info = group.get('musicInfo', {})
                        if music_info:
                            # Get main artists
                            for artist in music_info.get('artists', []):
                                artists.append(artist.get('name', ''))
                            # Also get 'with' artists if any
                            for artist in music_info.get('with', []):
                                artists.append(artist.get('name', ''))
                        
                        artist_str = ', '.join(artists) if artists else 'Various Artists'
                        
                        album_entry = {
                            'album_id': group.get('id'),
                            'album_name': group.get('name', ''),
                            'artist': artist_str,
                            'year': group.get('year', '')
                        }
                        all_albums.append(album_entry)
                    
                    # Check if more pages
                    if page >= resp.get('pages', 1):
                        break
                    page += 1
                    
            except Exception as e:
                print(f"   ❌ Error fetching collage {collage_id}: {e}")
                break
            
            await asyncio.sleep(0.2)  # Rate limit
        
        collage_info['albums'] = all_albums
        return collage_info
    
    async def build_complete_database(self, collages: List[Dict]) -> Dict:
        """Fetch contents for all collages and build searchable database"""
        print("📥 Step 2: Fetching contents of all collages via API...")
        print("   (This will take a while...)\n")
        
        database = {
            'collages': {},
            'artist_to_collages': {},  # artist_name -> [collage_ids]
            'album_to_collages': {},   # album_name -> [collage_ids]
            'stats': {
                'total_collages': 0,
                'total_albums': 0,
                'total_artists': 0
            },
            'last_updated': datetime.now().isoformat()
        }
        
        for i, collage in enumerate(collages, 1):
            print(f"   [{i}/{len(collages)}] Fetching collage #{collage['id']}: {collage['name'][:50]}...")
            
            contents = await self.fetch_collage_contents(collage['id'])
            
            # Store collage
            database['collages'][collage['id']] = {
                'name': contents.get('name', collage['name']),
                'albums': contents['albums']
            }
            
            # Build reverse indexes
            for album in contents['albums']:
                # Index by artist
                artist = album['artist'].lower()
                if artist not in database['artist_to_collages']:
                    database['artist_to_collages'][artist] = []
                if collage['id'] not in database['artist_to_collages'][artist]:
                    database['artist_to_collages'][artist].append(collage['id'])
                
                # Index by album
                album_name = album['album_name'].lower()
                if album_name not in database['album_to_collages']:
                    database['album_to_collages'][album_name] = []
                if collage['id'] not in database['album_to_collages'][album_name]:
                    database['album_to_collages'][album_name].append(collage['id'])
            
            # Progress update every 10 collages
            if i % 10 == 0:
                print(f"      Progress: {i}/{len(collages)} collages processed...")
        
        # Calculate stats
        database['stats']['total_collages'] = len(database['collages'])
        database['stats']['total_artists'] = len(database['artist_to_collages'])
        database['stats']['total_albums'] = len(database['album_to_collages'])
        
        return database
    
    def save_database(self, database: Dict):
        """Save the complete database to disk"""
        db_file = self.cache_dir / 'complete_collage_database.json'
        
        with open(db_file, 'w') as f:
            json.dump(database, f, indent=2)
        
        print(f"\n✅ Database saved to: {db_file}")
        print(f"\n📊 Database Statistics:")
        print(f"   Total collages: {database['stats']['total_collages']}")
        print(f"   Unique artists indexed: {database['stats']['total_artists']}")
        print(f"   Unique albums indexed: {database['stats']['total_albums']}")

async def main():
    # Credentials
    username = "rezivor"
    password = "Koolca00"
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    print("🔐 Building Complete Orpheus Collage Database")
    print("=" * 50)
    
    async with OrpheusCollageDatabase(username, password, api_key) as builder:
        # Login to website
        if not await builder.login():
            print("❌ Failed to login")
            return
        
        # Get all collage IDs
        collages = await builder.fetch_all_collage_ids()
        
        if not collages:
            print("❌ No collages found")
            return
        
        # Build complete database
        database = await builder.build_complete_database(collages)
        
        # Save it
        builder.save_database(database)
        
        print("\n✨ Database build complete!")
        print("   You can now use search_collage_db.py to search by artist or album")

if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ BeautifulSoup4 is required. Install it with:")
        print("   pip3 install beautifulsoup4")
        exit(1)
    
    asyncio.run(main())
