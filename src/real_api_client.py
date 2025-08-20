#!/usr/bin/env python3
"""
Real Orpheus API Implementation - Using Only Documented Endpoints
Based exactly on official API documentation
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
    Real Orpheus API client using only documented endpoints
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

    async def browse_torrents(self, 
                             searchstr: str = None,
                             artistname: str = None,
                             groupname: str = None,
                             page: int = 1,
                             **filters) -> Optional[Dict]:
        """
        Real API: ajax.php?action=browse
        
        From API docs: Torrent Search endpoint
        
        Args:
            searchstr: Search string
            artistname: Artist name filter
            groupname: Album/group name filter  
            page: Page number
            **filters: format, encoding, media, year, haslog, etc.
            
        Returns:
            API response with torrent groups and torrents
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
        if groupname:
            params['groupname'] = groupname
            
        # Add filters from API docs
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
        Real API: ajax.php?action=torrentgroup&id=<Torrent Group Id>
        
        Gets complete details of a torrent group (album release)
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
        
        Downloads .torrent file
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
        Find all releases of an album using REAL API endpoints
        
        This uses the browse API with artistname + groupname parameters.
        Each result group represents a different album release/edition.
        """
        
        # Use real browse API with specific artist/album parameters
        browse_results = await self.browse_torrents(
            artistname=artist,
            groupname=album
        )
        
        if not browse_results:
            return {"error": "No releases found"}
        
        releases = []
        
        # Process each group (each group = different release)
        for result in browse_results.get('results', []):
            group_id = result.get('groupId')
            
            # Get full details of this release using torrentgroup API
            group_details = await self.get_torrent_group(group_id)
            
            if group_details:
                group_info = group_details.get('group', {})
                torrents = group_details.get('torrents', [])
                
                release_info = {
                    'group_id': group_id,
                    'album_name': group_info.get('name', album),
                    'year': group_info.get('year', 0),
                    'record_label': group_info.get('recordLabel', ''),
                    'catalogue_number': group_info.get('catalogueNumber', ''),
                    'release_type': group_info.get('releaseType', 0),
                    'torrent_count': len(torrents),
                    'torrents': []
                }
                
                # Process torrents for this release
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
        """
        Filter and organize torrents by encoding preference
        """
        
        preferred_torrents = []
        fallback_torrents = []
        
        for torrent in torrents:
            format_str = torrent.get('format', '').lower()
            encoding_str = torrent.get('encoding', '').lower()
            
            # Check if matches preferred encoding
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
