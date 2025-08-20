#!/usr/bin/env python3
"""
Collage Discoverer - Core innovation that solves API limitation
Combines web scraping + API to find which collages contain albums/artists
"""

import asyncio
import json
import re
import aiohttp
import ssl
from pathlib import Path
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging


class OrpheusAlbumCollageSearcher:
    """
    The core innovation: Find collages containing albums by scraping + API
    
    This solves the fundamental limitation where Orpheus API doesn't let you
    search for artists/albums to find which collages they're in.
    """
    
    def __init__(self, username: str = None, password: str = None, api_key: str = None):
        # Load credentials from config if not provided
        config_path = Path.home() / '.orpheus' / 'config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.username = username or config.get('username')
                self.password = password or config.get('password') 
                self.api_key = api_key or config.get('api_key')
        else:
            self.username = username
            self.password = password
            self.api_key = api_key
            
        self.base_url = "https://orpheus.network"
        self.session = None
        self.logged_in = False

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
        """Login to Orpheus website for scraping"""
        if self.logged_in:
            return True
            
        login_url = f"{self.base_url}/login.php"
        login_data = {
            'username': self.username,
            'password': self.password,
            'keeplogged': '1'
        }

        try:
            async with self.session.post(login_url, data=login_data) as response:
                if response.status == 200:
                    # Check if we're redirected to index (successful login)
                    if 'index.php' in str(response.url) or response.url.path == '/':
                        self.logged_in = True
                        return True
                return False
        except Exception as e:
            logging.error(f"Login failed: {e}")
            return False

    async def search_albums_on_website(self, artist: str = None, album: str = None) -> List[Dict]:
        """
        Search for albums on website and extract collage information
        This is the core innovation - scraping what API can't provide
        """
        if not await self.login():
            raise Exception("Login failed")

        search_url = f"{self.base_url}/torrents.php"
        params = {'searchstr': ''}
        
        if artist and album:
            params['searchstr'] = f"{artist} {album}"
        elif artist:
            params['searchstr'] = artist
            params['artistname'] = artist
        elif album:
            params['searchstr'] = album
        
        albums_found = []
        
        try:
            async with self.session.get(search_url, params=params) as response:
                if response.status != 200:
                    return albums_found
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Parse search results to find torrent groups
                torrent_groups = soup.find_all('tr', class_='group')
                
                for group in torrent_groups:
                    album_info = await self._parse_album_from_group(group)
                    if album_info:
                        # Get detailed collage info for this album
                        collages = await self._get_album_collages(album_info['id'])
                        album_info['collages'] = collages
                        albums_found.append(album_info)
                        
        except Exception as e:
            logging.error(f"Search failed: {e}")
            
        return albums_found

    async def _parse_album_from_group(self, group_element) -> Optional[Dict]:
        """Parse album information from torrent group HTML"""
        try:
            # Extract group ID from links
            group_link = group_element.find('a', href=re.compile(r'torrents\.php\?id='))
            if not group_link:
                return None
                
            group_id_match = re.search(r'id=(\d+)', group_link['href'])
            if not group_id_match:
                return None
                
            group_id = int(group_id_match.group(1))
            
            # Extract artist and album name
            artist_elements = group_element.find_all('a', href=re.compile(r'artist\.php'))
            artists = [elem.text.strip() for elem in artist_elements] if artist_elements else ['Unknown']
            
            album_element = group_element.find('a', href=re.compile(r'torrents\.php\?id='))
            album_name = album_element.text.strip() if album_element else 'Unknown'
            
            # Extract year
            year_match = re.search(r'\[(\d{4})\]', group_element.text)
            year = int(year_match.group(1)) if year_match else None
            
            return {
                'id': group_id,
                'artist': ', '.join(artists),
                'album': album_name,
                'year': year,
                'url': f"{self.base_url}/torrents.php?id={group_id}"
            }
            
        except Exception as e:
            logging.error(f"Failed to parse album: {e}")
            return None

    async def _get_album_collages(self, group_id: int) -> List[Dict]:
        """
        Get collages for a specific album by scraping its page
        This is where the magic happens - extracting collage info from album pages
        """
        album_url = f"{self.base_url}/torrents.php?id={group_id}"
        collages = []
        
        try:
            async with self.session.get(album_url) as response:
                if response.status != 200:
                    return collages
                    
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Look for collage links in the album page
                collage_links = soup.find_all('a', href=re.compile(r'collages\.php\?id='))
                
                for link in collage_links:
                    collage_id_match = re.search(r'id=(\d+)', link['href'])
                    if collage_id_match:
                        collage_id = int(collage_id_match.group(1))
                        collage_name = link.text.strip()
                        
                        # Get detailed collage info via API
                        collage_details = await self._get_collage_details_api(collage_id)
                        
                        collages.append({
                            'id': collage_id,
                            'name': collage_name,
                            'url': f"{self.base_url}/collages.php?id={collage_id}",
                            'details': collage_details
                        })
                        
        except Exception as e:
            logging.error(f"Failed to get collages for group {group_id}: {e}")
            
        return collages

    async def _get_collage_details_api(self, collage_id: int) -> Optional[Dict]:
        """Get detailed collage information via API"""
        if not self.api_key:
            return None
            
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusCollageTools/1.0'
        }
        params = {
            'action': 'collage',
            'id': collage_id
        }
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
        except Exception as e:
            logging.error(f"API call failed for collage {collage_id}: {e}")
            
        return None

    async def find_album_collages(self, artist: str = None, album: str = None, limit: int = 50) -> List[Dict]:
        """
        Main method: Find which collages contain specific albums/artists
        
        This combines web scraping + API calls to solve the core limitation
        """
        logging.info(f"🔍 Searching for collages containing: {artist} - {album}")
        
        # Search albums on website (includes collage discovery)
        albums = await self.search_albums_on_website(artist=artist, album=album)
        
        # Filter and limit results
        results = []
        for album_info in albums[:limit]:
            if album_info.get('collages'):
                results.append({
                    'album': album_info,
                    'collages': album_info['collages'],
                    'total_collages': len(album_info['collages'])
                })
        
        logging.info(f"✅ Found {len(results)} albums with collage memberships")
        return results
