#!/usr/bin/env python3
"""
Test if album/artist pages on Orpheus show collage membership
Then use those collage IDs with the API
"""

import asyncio
import json
import re
from pathlib import Path
import aiohttp
import ssl
from bs4 import BeautifulSoup
from typing import List, Dict

class OrpheusCollageSearcher:
    def __init__(self, username: str, password: str, api_key: str):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.base_url = "https://orpheus.network"
        self.session = None
        
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
                        print("✅ Successfully logged in")
                        return True
        
        print("❌ Login failed")
        return False
    
    async def search_album(self, artist_name: str, album_name: str) -> Dict:
        """Search for an album and get its group ID"""
        print(f"\n🔍 Searching for '{artist_name} - {album_name}'...")
        
        # Search using the torrents search
        search_url = f"{self.base_url}/torrents.php"
        params = {
            'artistname': artist_name,
            'groupname': album_name,
            'action': 'advanced'
        }
        
        async with self.session.get(search_url, params=params) as response:
            if response.status != 200:
                print(f"❌ Search failed: {response.status}")
                return None
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find torrent group links
            group_links = soup.find_all('a', href=re.compile(r'torrents\.php\?id=\d+'))
            
            for link in group_links:
                # Check if this is the album we're looking for
                if album_name.lower() in link.text.lower():
                    group_id = re.search(r'id=(\d+)', link['href'])
                    if group_id:
                        return {
                            'group_id': int(group_id.group(1)),
                            'name': link.text.strip(),
                            'url': f"{self.base_url}/torrents.php?id={group_id.group(1)}"
                        }
        
        print(f"❌ Album not found")
        return None
    
    async def get_album_collages(self, group_id: int) -> List[Dict]:
        """Scrape album page to find which collages it's in"""
        print(f"\n📄 Fetching album page for group ID {group_id}...")
        
        album_url = f"{self.base_url}/torrents.php?id={group_id}"
        
        async with self.session.get(album_url) as response:
            if response.status != 200:
                print(f"❌ Failed to fetch album page: {response.status}")
                return []
            
            html = await response.text()
            
            # Save HTML for debugging
            with open('/Users/cameronbrooks/.orpheus/album_page.html', 'w') as f:
                f.write(html)
            print("   Saved HTML to album_page.html for inspection")
            
            soup = BeautifulSoup(html, 'html.parser')
            
            collages = []
            
            # Method 1: Look for a "Collages" section or box
            collage_box = soup.find('div', class_='box_collages')
            if not collage_box:
                # Try alternate selectors
                collage_box = soup.find('div', {'id': 'collages'})
                if not collage_box:
                    # Look for any heading with "Collage" 
                    for heading in soup.find_all(['h2', 'h3', 'div'], class_='head'):
                        if heading and 'collage' in heading.text.lower():
                            collage_box = heading.parent
                            break
            
            if collage_box:
                print("✅ Found collages section!")
                # Find all collage links within this section
                collage_links = collage_box.find_all('a', href=re.compile(r'collages\.php\?id=\d+'))
                
                for link in collage_links:
                    collage_id = re.search(r'id=(\d+)', link['href'])
                    if collage_id:
                        collages.append({
                            'id': int(collage_id.group(1)),
                            'name': link.text.strip()
                        })
                        print(f"   Found collage: {link.text.strip()} (ID: {collage_id.group(1)})")
            
            # Method 2: Search entire page for collage links
            if not collages:
                print("⚠️  No collages box found, searching entire page...")
                
                # Look for text like "This album is in X collage(s)"
                text_content = soup.get_text()
                if 'collage' in text_content.lower():
                    print("   Found 'collage' mentioned in page")
                    
                    # Find all collage links
                    all_collage_links = soup.find_all('a', href=re.compile(r'collages\.php\?id=\d+'))
                    
                    for link in all_collage_links:
                        collage_id = re.search(r'id=(\d+)', link['href'])
                        if collage_id:
                            # Skip if it's "Add to collage" type link
                            if 'add' not in link.text.lower():
                                collages.append({
                                    'id': int(collage_id.group(1)),
                                    'name': link.text.strip()
                                })
                                print(f"   Found collage link: {link.text.strip()} (ID: {collage_id.group(1)})")
            
            # Method 3: Look in sidebar
            if not collages:
                sidebar = soup.find('div', class_='sidebar')
                if sidebar:
                    print("   Checking sidebar...")
                    collage_links = sidebar.find_all('a', href=re.compile(r'collages\.php\?id=\d+'))
                    for link in collage_links:
                        collage_id = re.search(r'id=(\d+)', link['href'])
                        if collage_id:
                            collages.append({
                                'id': int(collage_id.group(1)),
                                'name': link.text.strip()
                            })
                            print(f"   Found in sidebar: {link.text.strip()} (ID: {collage_id.group(1)})")
            
            return collages
    
    async def get_collage_details(self, collage_id: int) -> Dict:
        """Use API to get full collage details"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'CollageSearcher/1.0'
        }
        
        params = {
            'action': 'collage',
            'id': collage_id,
            'page': 1
        }
        
        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('status') == 'success':
                    return data['response']
        
        return None

async def main():
    # Credentials
    username = "rezivor"
    password = "Koolca00"
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    async with OrpheusCollageSearcher(username, password, api_key) as searcher:
        # Login
        if not await searcher.login():
            return
        
        # Search for Critical Beatdown
        album = await searcher.search_album("Ultramagnetic MC's", "Critical Beatdown")
        
        if album:
            print(f"\n✅ Found album: {album['name']}")
            print(f"   Group ID: {album['group_id']}")
            print(f"   URL: {album['url']}")
            
            # Get collages containing this album
            collages = await searcher.get_album_collages(album['group_id'])
            
            if collages:
                print(f"\n🎯 Album is in {len(collages)} collage(s)!")
                
                # Get full details for each collage via API
                for collage in collages:
                    print(f"\n📥 Fetching details for collage #{collage['id']}: {collage['name']}")
                    details = await searcher.get_collage_details(collage['id'])
                    
                    if details:
                        print(f"   Category: {details.get('collageCategoryName')}")
                        print(f"   Total albums: {len(details.get('torrentGroupIDList', []))}")
                        print(f"   Description: {details.get('description_raw', '')[:200]}...")
            else:
                print("\n❌ No collages found for this album (or not displayed on page)")
        else:
            print("\n❌ Album not found")

if __name__ == "__main__":
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ BeautifulSoup4 is required. Install it with:")
        print("   pip3 install beautifulsoup4")
        exit(1)
    
    asyncio.run(main())
