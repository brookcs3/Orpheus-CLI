#!/usr/bin/env python3
"""
Fetch all collages from Orpheus website using the actual Gazelle parameters
Based on the Gazelle source code at /Users/cameronbrooks/Gazelle
"""

import asyncio
import json
import re
from pathlib import Path
from datetime import datetime
import aiohttp
import ssl
from bs4 import BeautifulSoup
from typing import Dict, List
import time

class OrpheusCollageScaper:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.base_url = "https://orpheus.network"
        self.session = None
        self.cache_dir = Path.home() / '.orpheus' / 'collage_db'
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
        """Login to Orpheus and get session cookie"""
        login_url = f"{self.base_url}/login.php"
        
        # Login with provided credentials
        login_data = {
            'username': self.username,
            'password': self.password,
            'keeplogged': '1',
            'login': 'Log in'
        }
        
        async with self.session.post(login_url, data=login_data, allow_redirects=False) as response:
            # Check cookies for session
            if 'session' in response.cookies or response.status in [302, 303]:
                # Verify we're logged in
                async with self.session.get(f"{self.base_url}/index.php") as index_response:
                    text = await index_response.text()
                    if 'logout.php' in text or 'username' in text.lower():
                        print("✅ Successfully logged in to Orpheus")
                        return True
        
        print("❌ Login failed. Check your credentials.")
        return False
    
    async def fetch_collages_page(self, page: int = 1, search_params: Dict = None) -> tuple[List[Dict], bool]:
        """
        Fetch a single page of collages using Gazelle parameters
        Returns: (collages_list, has_next_page)
        """
        url = f"{self.base_url}/collages.php"
        
        # Use actual Gazelle parameters from browse.php
        params = {
            'page': page
        }
        
        if search_params:
            params.update(search_params)
        
        async with self.session.get(url, params=params) as response:
            if response.status != 200:
                print(f"❌ Failed to fetch page {page}: {response.status}")
                return [], False
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            collages = []
            
            # Find the collage table using the exact class from the template
            collage_table = soup.find('table', {'class': 'collage_table'})
            if not collage_table:
                # Try alternate selector
                collage_table = soup.find('table', class_=lambda x: x and 'collage_table' in x)
            
            if collage_table:
                # Parse each row (skip header)
                rows = collage_table.find_all('tr')
                for row in rows[1:]:  # Skip header row
                    cells = row.find_all('td')
                    if len(cells) >= 6:  # Based on template: category, name/time, torrents, subscribers, updated, author
                        # Category cell
                        category_cell = cells[0]
                        category = category_cell.get_text(strip=True)
                        
                        # Info cell (contains name and tags)
                        info_cell = cells[1]
                        collage_link = info_cell.find('a', href=re.compile(r'collages\.php\?id=\d+'))
                        
                        if collage_link:
                            # Extract ID from URL
                            collage_id = re.search(r'id=(\d+)', collage_link['href'])
                            if collage_id:
                                collage_info = {
                                    'id': int(collage_id.group(1)),
                                    'name': collage_link.get_text(strip=True),
                                    'category': category,
                                    'url': f"{self.base_url}/collages.php?id={collage_id.group(1)}"
                                }
                                
                                # Extract tags
                                tags_div = info_cell.find('div', class_='tags')
                                if tags_div:
                                    tags = [a.get_text(strip=True) for a in tags_div.find_all('a')]
                                    collage_info['tags'] = tags
                                
                                # Torrent count
                                torrent_cell = cells[2]
                                torrent_text = torrent_cell.get_text(strip=True).replace(',', '')
                                if torrent_text.isdigit():
                                    collage_info['torrent_count'] = int(torrent_text)
                                
                                # Subscriber count
                                subscriber_cell = cells[3]
                                subscriber_text = subscriber_cell.get_text(strip=True).replace(',', '')
                                if subscriber_text.isdigit():
                                    collage_info['subscribers'] = int(subscriber_text)
                                
                                # Updated time
                                updated_cell = cells[4]
                                collage_info['updated'] = updated_cell.get_text(strip=True)
                                
                                # Author
                                author_cell = cells[5]
                                author_link = author_cell.find('a')
                                if author_link:
                                    collage_info['author'] = author_link.get_text(strip=True)
                                
                                collages.append(collage_info)
            
            # Check if there's a next page by looking for pagination
            has_next = False
            linkbox = soup.find('div', class_='linkbox')
            if linkbox:
                # Look for "Next >" link
                next_link = linkbox.find('a', string=re.compile(r'Next'))
                has_next = next_link is not None
            
            return collages, has_next
    
    async def fetch_all_collages(self) -> List[Dict]:
        """Fetch all collages from all pages"""
        all_collages = []
        page = 1
        
        print("📥 Fetching all collages from Orpheus...")
        
        while True:
            print(f"   Fetching page {page}...")
            collages, has_next = await self.fetch_collages_page(page)
            
            if not collages:
                if page == 1:
                    print("❌ No collages found. Check if you're logged in properly.")
                break
            
            all_collages.extend(collages)
            print(f"   Found {len(collages)} collages (total: {len(all_collages)})")
            
            if not has_next:
                break
            
            page += 1
            await asyncio.sleep(1)  # Be nice to the server
        
        return all_collages
    
    def save_database(self, collages: List[Dict]):
        """Save the collage database locally"""
        db_file = self.cache_dir / 'collage_database.json'
        
        database = {
            'collages': collages,
            'total': len(collages),
            'last_updated': datetime.now().isoformat(),
            'by_category': {},
            'by_id': {},
            'by_tag': {}
        }
        
        # Create indexes
        for collage in collages:
            # Index by ID
            database['by_id'][str(collage['id'])] = collage
            
            # Index by category
            category = collage.get('category', 'Unknown')
            if category not in database['by_category']:
                database['by_category'][category] = []
            database['by_category'][category].append(collage)
            
            # Index by tags
            for tag in collage.get('tags', []):
                if tag not in database['by_tag']:
                    database['by_tag'][tag] = []
                database['by_tag'][tag].append(collage['id'])
        
        with open(db_file, 'w') as f:
            json.dump(database, f, indent=2)
        
        print(f"\n✅ Saved database with {len(collages)} collages to {db_file}")
        
        # Print summary
        print("\n📊 Summary by category:")
        for category, items in sorted(database['by_category'].items()):
            print(f"   {category}: {len(items)} collages")
        
        print(f"\n📊 Total unique tags: {len(database['by_tag'])}")

async def main():
    """Main function to fetch all collages"""
    import sys
    
    # Use the provided credentials
    username = "rezivor"
    password = "Koolca00"
    
    print("🔐 Logging in to Orpheus...")
    
    async with OrpheusCollageScaper(username, password) as scraper:
        # Login
        if not await scraper.login():
            print("❌ Failed to login. Check your credentials.")
            sys.exit(1)
        
        # Fetch all collages
        collages = await scraper.fetch_all_collages()
        
        if collages:
            # Save the database
            scraper.save_database(collages)
            
            print(f"\n✨ Successfully fetched {len(collages)} collages!")
            print("You can now use search_collages.py to search this local database")
        else:
            print("❌ No collages found. The HTML structure might have changed.")

if __name__ == "__main__":
    # Check if BeautifulSoup is installed
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ BeautifulSoup4 is required. Install it with:")
        print("   pip3 install beautifulsoup4")
        exit(1)
    
    asyncio.run(main())
