#!/usr/bin/env python3
"""
Real Orpheus API Client - Correct Field Names
album = title (NOT groupname)
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path
from typing import Dict, List, Optional
import logging


class OrpheusAPIClient:
    """
    Real Orpheus API client using correct field names
    album = title (NOT groupname)
    """
    
    def __init__(self, api_key: str = None):
        config_path = Path.home() / '.orpheus' / 'config.json'
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.api_key = api_key or config.get('api_key')
        else:
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

    async def search_torrents(self, 
                             searchstr: str = None,
                             artistname: str = None,
                             title: str = None,  # album title - NOT groupname
                             page: int = 1,
                             **filters) -> Optional[Dict]:
        """
        Search torrents using correct API parameters
        
        Args:
            searchstr: Free-form search string
            artistname: Artist name (API parameter)
            title: Album title (API parameter - NOT groupname)
            page: Page number
            **filters: Additional API filters
            
        Returns:
            API response from browse endpoint
        """
        
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusAPIClient/1.0'
        }
        
        params = {'action': 'browse', 'page': page}
        
        if searchstr:
            params['searchstr'] = searchstr
        if artistname:
            params['artistname'] = artistname
        if title:
            params['title'] = title  # Album title - correct API parameter
            
        # Add additional filters
        params.update(filters)
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
        except Exception as e:
            logging.error(f"Browse API failed: {e}")
            
        return None

    async def get_torrent_group(self, group_id: int) -> Optional[Dict]:
        """
        Real API: ajax.php?action=torrentgroup&id=<Group Id>
        """
        
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusAPIClient/1.0'
        }
        
        params = {
            'action': 'torrentgroup',
            'id': group_id
        }
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
        except Exception as e:
            logging.error(f"Torrent group API failed: {e}")
            
        return None

    async def download_torrent(self, torrent_id: int, use_token: bool = False) -> Optional[bytes]:
        """
        Real API: ajax.php?action=download&id=<Torrent Id>
        """
        
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusAPIClient/1.0'
        }
        
        params = {
            'action': 'download',
            'id': torrent_id
        }
        
        if use_token:
            params['usetoken'] = 'true'
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    content_type = response.headers.get('content-type', '')
                    if 'application/x-bittorrent' in content_type:
                        return await response.read()
        except Exception as e:
            logging.error(f"Download API failed: {e}")
            
        return None

    async def find_album_releases(self, artist: str, album: str) -> Dict:
        """
        Find all releases of an album
        
        Args:
            artist: Artist name
            album: Album title
        """
        
        # Use browse API with artistname + title (NOT groupname)
        search_results = await self.search_torrents(artistname=artist, title=album)
        
        if not search_results:
            return {"error": "No releases found"}
        
        releases = []
        
        # Process results 
        for result in search_results.get('results', []):
            group_id = result.get('groupId')
            
            # Get detailed info using torrentgroup API
            group_details = await self.get_torrent_group(group_id)
            
            if group_details:
                group_info = group_details.get('group', {})
                torrents = group_details.get('torrents', [])
                
                # Extract release info using actual API response field names
                release_info = {
                    'group_id': group_id,
                    'album_title': group_info.get('name', album),        # From API response
                    'year': group_info.get('year', 0),                   # From API response
                    'record_label': group_info.get('recordLabel', ''),   # From API response
                    'catalogue_number': group_info.get('catalogueNumber', ''), # From API response
                    'release_type': group_info.get('releaseType', 0),    # From API response
                    'torrent_count': len(torrents),
                    'torrents': []
                }
                
                # Process torrents using actual API response field names
                for torrent in torrents:
                    torrent_info = {
                        'torrent_id': torrent.get('id'),          
                        'format': torrent.get('format', ''),      
                        'encoding': torrent.get('encoding', ''),  
                        'media': torrent.get('media', ''),        
                        'hasLog': torrent.get('hasLog', False),   
                        'logScore': torrent.get('logScore', 0),   
                        'hasCue': torrent.get('hasCue', False),   
                        'seeders': torrent.get('seeders', 0),     
                        'size': torrent.get('size', 0),           
                        'scene': torrent.get('scene', False)      
                    }
                    release_info['torrents'].append(torrent_info)
                
                releases.append(release_info)
        
        return {
            "success": True,
            "artist": artist,
            "album": album,
            "total_releases": len(releases),
            "releases": releases
        }

    def filter_torrents_by_encoding(self, torrents: List[Dict], 
                                   preferred_encoding: str,
                                   fallback_strategy: str) -> Dict:
        """Filter torrents by encoding preference"""
        
        preferred_torrents = []
        fallback_torrents = []
        
        for torrent in torrents:
            format_str = torrent.get('format', '').lower()
            encoding_str = torrent.get('encoding', '').lower()
            
            if self._matches_encoding(format_str, encoding_str, preferred_encoding):
                preferred_torrents.append(torrent)
            else:
                fallback_torrents.append(torrent)
        
        # Sort fallback by quality strategy
        if fallback_strategy == "highest":
            fallback_torrents.sort(key=self._get_quality_score, reverse=True)
        else:  # "lowest"
            fallback_torrents.sort(key=self._get_quality_score, reverse=False)
        
        return {
            "preferred_torrents": preferred_torrents,
            "fallback_torrents": fallback_torrents,
            "total_torrents": len(torrents)
        }

    def _matches_encoding(self, format_str: str, encoding_str: str, preferred: str) -> bool:
        """Check if torrent matches preferred encoding"""
        preferred = preferred.lower().strip()
        
        patterns = {
            '320': format_str == 'mp3' and '320' in encoding_str,
            'v0': format_str == 'mp3' and 'v0' in encoding_str,
            'v1': format_str == 'mp3' and 'v1' in encoding_str,
            'v2': format_str == 'mp3' and 'v2' in encoding_str,
            'flac': format_str == 'flac',
            'lossless': 'lossless' in encoding_str,
            '24bit': '24bit' in encoding_str
        }
        
        return (patterns.get(preferred, False) or 
                preferred in encoding_str or 
                preferred in format_str)

    def _get_quality_score(self, torrent: Dict) -> int:
        """Quality scoring for fallback sorting"""
        format_str = torrent.get('format', '').upper()
        encoding_str = torrent.get('encoding', '').upper()
        
        format_scores = {'FLAC': 100, 'MP3': 80, 'AAC': 60}
        encoding_scores = {
            '24BIT LOSSLESS': 95, 'LOSSLESS': 90, '320': 85,
            'V0 (VBR)': 83, 'V1 (VBR)': 80, 'V2 (VBR)': 70
        }
        
        base_score = format_scores.get(format_str, 30)
        encoding_bonus = encoding_scores.get(encoding_str, 20)
        
        # Log/cue bonuses  
        quality_bonus = 0
        if torrent.get('hasLog') and torrent.get('logScore', 0) == 100:
            quality_bonus += 10
        if torrent.get('hasCue'):
            quality_bonus += 3
            
        return base_score + encoding_bonus + quality_bonus
