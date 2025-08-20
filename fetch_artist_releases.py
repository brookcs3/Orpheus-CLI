#!/usr/bin/env python3
"""
Fetch artist releases from Orpheus and create torrent_info.json
"""

import asyncio
import aiohttp
import json
import argparse
from pathlib import Path

class OrpheusArtistFetcher:
    def __init__(self, api_key=None, username=None, password=None):
        self.base_url = "https://orpheus.network"
        config = self.load_config()
        self.api_key = api_key or config.get('api_key')
        self.username = username or config.get('username')
        self.password = password or config.get('password')
        self.session = None

    def load_config(self):
        """Load config from file"""
        config_file = Path.home() / '.orpheus' / 'config.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}

    def load_api_key(self):
        """Load API key from config file"""
        return self.load_config().get('api_key')

    async def create_session(self):
        """Create aiohttp session with SSL context"""
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=ssl_context),
            timeout=aiohttp.ClientTimeout(total=30)
        )

    async def login(self):
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
                return True
        return False

    async def fetch_artist_data(self, artist_id):
        """Fetch artist data from Orpheus API"""
        if not self.session:
            await self.create_session()

        url = f"{self.base_url}/ajax.php"
        params = {
            'action': 'artist',
            'id': artist_id
        }
        
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'token {self.api_key}'

        print(f"🎵 Fetching artist data for ID {artist_id}...")
        
        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"❌ Failed to fetch artist data: {response.status}")
                print(f"Response: {await response.text()}")
                return None

    async def fetch_torrent_group(self, group_id):
        """Fetch detailed torrent group information"""
        if not self.session:
            await self.create_session()

        url = f"{self.base_url}/ajax.php"
        params = {
            'action': 'torrentgroup',
            'id': group_id
        }
        
        headers = {}
        if self.api_key:
            headers['Authorization'] = f'token {self.api_key}'

        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"❌ Failed to fetch group {group_id}: {response.status}")
                return None

    def create_output_directory(self, artist_name):
        """Create output directory for artist"""
        safe_name = "".join(c for c in artist_name if c.isalnum() or c in (' ', '-', '_')).strip()
        output_path = Path.home() / '.orpheus' / f'artist_{safe_name}'
        output_path.mkdir(exist_ok=True)
        return output_path

    async def process_artist(self, artist_id, max_releases=None):
        """Process artist and create torrent_info.json"""
        try:
            # Fetch artist data
            artist_data = await self.fetch_artist_data(artist_id)
            if not artist_data or 'response' not in artist_data:
                print("❌ No artist data received")
                return

            response = artist_data['response']
            artist_name = response.get('name', f'Artist_{artist_id}')
            
            print(f"🎤 Artist: {artist_name}")
            print(f"📀 Found {len(response.get('torrentgroup', []))} releases")

            # Create output directory
            output_path = self.create_output_directory(artist_name)
            
            # Process torrent groups
            torrent_groups = []
            groups = response.get('torrentgroup', [])
            
            if max_releases:
                groups = groups[:max_releases]
                print(f"📋 Limited to first {max_releases} releases")

            for i, group in enumerate(groups, 1):
                print(f"   {i}/{len(groups)}: {group.get('groupName', 'Unknown')} ({group.get('groupYear', 'Unknown')})")
                
                # Fetch detailed group data
                detailed_group = await self.fetch_torrent_group(group['groupId'])
                if detailed_group and 'response' in detailed_group:
                    torrent_groups.append(detailed_group['response'])
                
                # Small delay to be nice to the API
                await asyncio.sleep(0.5)

            # Create torrent_info.json structure
            torrent_info = {
                'artist_id': artist_id,
                'artist_name': artist_name,
                'artist_info': response,
                'total_releases': len(torrent_groups),
                'torrent_groups': torrent_groups
            }

            # Save to JSON file
            info_file = output_path / 'torrent_info.json'
            with open(info_file, 'w', encoding='utf-8') as f:
                json.dump(torrent_info, f, indent=2, ensure_ascii=False)

            print(f"💾 Saved artist info to {info_file}")
            print(f"📁 Output directory: {output_path}")
            print(f"✅ Successfully processed {len(torrent_groups)} releases")

        except Exception as e:
            print(f"❌ Error processing artist: {e}")

    async def close(self):
        """Close session"""
        if self.session:
            await self.session.close()

async def main():
    parser = argparse.ArgumentParser(description="Fetch artist releases from Orpheus")
    parser.add_argument('artist_id', type=int, help='Artist ID to fetch')
    parser.add_argument('--max', type=int, help='Maximum number of releases to fetch')
    parser.add_argument('--api-key', help='API key (or use config file)')

    args = parser.parse_args()

    fetcher = OrpheusArtistFetcher(api_key=args.api_key)
    
    try:
        await fetcher.process_artist(args.artist_id, args.max)
    finally:
        await fetcher.close()

if __name__ == "__main__":
    asyncio.run(main())
