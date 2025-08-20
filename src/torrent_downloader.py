#!/usr/bin/env python3
"""
Torrent Downloader with Intelligent Encoding Preferences
Handles the smart downloading functionality from your existing system
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path
from typing import List, Dict, Optional
import logging


class OrpheusCollageDownloader:
    """
    Download torrents from collages with intelligent encoding preferences
    Implements your exact requirements: 320 CBR preferred, FLAC fallback, one per album
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

    async def get_collage_info(self, collage_id: int) -> Optional[Dict]:
        """Get collage information via API"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusCollageDownloader/1.0'
        }
        params = {
            'action': 'collage',
            'id': collage_id
        }
        
        async with self.session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data.get('status') == 'success':
                    return data['response']
        return None

    async def get_all_collage_torrents(self, collage_id: int) -> List[Dict]:
        """Get all torrents from all pages of a collage"""
        all_torrents = []
        page = 1
        
        logging.info(f"📥 Fetching collage #{collage_id} torrents...")
        
        while True:
            url = f"{self.base_url}/ajax.php"
            headers = {
                'Authorization': f'token {self.api_key}',
                'User-Agent': 'OrpheusCollageDownloader/1.0'
            }
            params = {
                'action': 'collage',
                'id': collage_id,
                'page': page
            }
            
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    break
                    
                data = await response.json()
                if data.get('status') != 'success':
                    break
                    
                resp = data['response']
                torrentgroups = resp.get('torrentgroups', [])
                
                if not torrentgroups:
                    break
                
                page_torrents = []
                for item in torrentgroups:
                    group = item.get('group', {})
                    torrents = item.get('torrents', [])
                    
                    # Extract artist names
                    artists = []
                    music_info = group.get('musicInfo', {})
                    if music_info:
                        for artist in music_info.get('artists', []):
                            artists.append(artist.get('name', ''))
                    
                    artist_str = ', '.join(artists) if artists else 'Unknown Artist'
                    
                    for torrent in torrents:
                        torrent_info = {
                            'torrent_id': torrent.get('id'),
                            'group_id': group.get('id'),
                            'artist': artist_str,
                            'album': group.get('name', 'Unknown Album'),
                            'year': group.get('year', 0),
                            'format': torrent.get('format', ''),
                            'encoding': torrent.get('encoding', ''),
                            'media': torrent.get('media', ''),
                            'hasLog': torrent.get('hasLog', False),
                            'logScore': torrent.get('logScore', 0),
                            'hasCue': torrent.get('hasCue', False),
                            'seeders': torrent.get('seeders', 0),
                            'leechers': torrent.get('leechers', 0),
                            'snatched': torrent.get('snatched', 0),
                            'size': torrent.get('size', 0),
                            'time': torrent.get('time', ''),
                            'scene': torrent.get('scene', False)
                        }
                        page_torrents.append(torrent_info)
                
                all_torrents.extend(page_torrents)
                logging.info(f"Page {page}: Found {len(page_torrents)} torrents")
                
                # Check if there are more pages
                if page >= resp.get('pages', 1):
                    break
                    
                page += 1
        
        logging.info(f"✅ Total torrents found: {len(all_torrents)}")
        return all_torrents

    def select_best_torrent(self, torrents: List[Dict], encoding_prefs: List[str]) -> Dict:
        """
        Select best torrent based on your exact encoding preferences
        Implements the intelligent quality hierarchy from your system
        """
        if not torrents:
            return None
        
        # Quality scoring based on Gazelle's hierarchy (from your system)
        quality_scores = {
            # FLAC variants (highest quality)
            ('FLAC', '24bit Lossless', 'Vinyl'): 10,
            ('FLAC', '24bit Lossless', 'DVD'): 9,
            ('FLAC', '24bit Lossless', 'SACD'): 9,
            ('FLAC', '24bit Lossless', 'WEB'): 8,
            ('FLAC', '24bit Lossless'): 8,
            ('FLAC', 'Lossless', 'log_100_cue'): 7,
            ('FLAC', 'Lossless', 'log_100'): 6,
            ('FLAC', 'Lossless', 'log'): 5,
            ('FLAC', 'Lossless', 'WEB'): 4,
            ('FLAC', 'Lossless'): 4,
            
            # MP3 CBR (preferred for consistency)
            ('MP3', '320'): 15,
            ('MP3', '256'): 12,
            ('MP3', '224'): 11,
            ('MP3', '192'): 10,
            
            # MP3 VBR High Quality
            ('MP3', 'V0 (VBR)'): 14,
            ('MP3', 'APX (VBR)'): 13,
            ('MP3', 'V1 (VBR)'): 12,
            
            # MP3 VBR Lower Quality
            ('MP3', 'V2 (VBR)'): 9,
            ('MP3', 'APS (VBR)'): 8,
            
            # Others
            ('AAC', '320'): 6,
            ('AAC', '256'): 5,
            ('DTS', ''): 3,
        }
        
        def get_torrent_score(torrent):
            format_str = torrent.get('format', '')
            encoding_str = torrent.get('encoding', '')
            media_str = torrent.get('media', '')
            has_log = torrent.get('hasLog', False)
            log_score = torrent.get('logScore', 0)
            has_cue = torrent.get('hasCue', False)
            
            # Special handling for FLAC with logs
            if format_str == 'FLAC' and encoding_str == 'Lossless':
                if has_log and log_score == 100 and has_cue:
                    key = ('FLAC', 'Lossless', 'log_100_cue')
                elif has_log and log_score == 100:
                    key = ('FLAC', 'Lossless', 'log_100')
                elif has_log:
                    key = ('FLAC', 'Lossless', 'log')
                elif media_str == 'WEB':
                    key = ('FLAC', 'Lossless', 'WEB')
                else:
                    key = ('FLAC', 'Lossless')
            elif format_str == 'FLAC' and encoding_str == '24bit Lossless':
                key = ('FLAC', '24bit Lossless', media_str)
                if key not in quality_scores:
                    key = ('FLAC', '24bit Lossless')
            else:
                key = (format_str, encoding_str)
            
            base_score = quality_scores.get(key, 0)
            
            # Apply preference matching
            pref_bonus = 0
            for i, pref in enumerate(encoding_prefs):
                if self.matches_preference(pref, format_str, encoding_str, media_str, has_log, log_score, has_cue):
                    pref_bonus = 100 - i
                    break
            
            # Quality bonuses
            quality_bonus = 0
            if has_log and log_score == 100:
                quality_bonus += 2
            elif has_log:
                quality_bonus += 1
            if has_cue:
                quality_bonus += 1
            
            # Seeder bonus
            seeder_bonus = min(torrent.get('seeders', 0) / 10, 5)
            
            return base_score + pref_bonus + quality_bonus + seeder_bonus
        
        return max(torrents, key=get_torrent_score)

    def matches_preference(self, pref: str, format_str: str, encoding_str: str, 
                          media_str: str, has_log: bool, log_score: int, has_cue: bool) -> bool:
        """Check if torrent matches preference string"""
        pref = pref.lower().strip()
        format_lower = format_str.lower()
        encoding_lower = encoding_str.lower()
        media_lower = media_str.lower()
        
        patterns = {
            '320': format_lower == 'mp3' and '320' in encoding_lower,
            '320 cbr': format_lower == 'mp3' and encoding_lower == '320',
            'v0': format_lower == 'mp3' and 'v0' in encoding_lower,
            'v0 vbr': format_lower == 'mp3' and encoding_lower == 'v0 (vbr)',
            'v1': format_lower == 'mp3' and 'v1' in encoding_lower,
            'v2': format_lower == 'mp3' and 'v2' in encoding_lower,
            'flac': format_lower == 'flac',
            'flac lossless': format_lower == 'flac' and 'lossless' in encoding_lower,
            'flac 24bit': format_lower == 'flac' and '24bit' in encoding_lower,
            'flac log': format_lower == 'flac' and has_log,
            'flac log 100': format_lower == 'flac' and has_log and log_score == 100,
            'flac log cue': format_lower == 'flac' and has_log and has_cue,
            'flac vinyl': format_lower == 'flac' and media_lower == 'vinyl',
            'flac cd': format_lower == 'flac' and media_lower == 'cd',
            'flac web': format_lower == 'flac' and media_lower == 'web',
        }
        
        return patterns.get(pref, False)

    async def download_collage_torrents(self, collage_id: int, output_dir: str = None, 
                                      format_filter: str = None, max_downloads: int = None,
                                      encoding_prefs: List[str] = None, one_per_album: bool = True,
                                      delay: float = 2.0) -> Dict:
        """
        Download torrents with your exact requirements:
        - 320 CBR preferred, FLAC fallback  
        - One torrent per album
        - All albums included
        """
        
        # Default encoding preferences (your exact specification)
        if encoding_prefs is None:
            encoding_prefs = ['320', 'FLAC Lossless', 'FLAC Log 100', 'FLAC Log', 'FLAC', 'V0']
        
        # Get collage info
        collage_info = await self.get_collage_info(collage_id)
        if not collage_info:
            return {"success": False, "error": "Could not fetch collage info"}
        
        collage_name = collage_info.get('name', f'Collage_{collage_id}')
        
        # Set up output directory
        if not output_dir:
            output_dir = f"collage_{collage_id}_{self.sanitize_filename(collage_name)}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get all torrents
        all_torrents = await self.get_all_collage_torrents(collage_id)
        if not all_torrents:
            return {"success": False, "error": "No torrents found"}
        
        # Group by album if one_per_album
        if one_per_album:
            albums = {}
            for torrent in all_torrents:
                group_id = torrent['group_id']
                if group_id not in albums:
                    albums[group_id] = {
                        'artist': torrent['artist'],
                        'album': torrent['album'],
                        'year': torrent['year'],
                        'torrents': []
                    }
                albums[group_id]['torrents'].append(torrent)
            
            # Select best torrent for each album
            selected_torrents = []
            for group_id, album_data in albums.items():
                best_torrent = self.select_best_torrent(album_data['torrents'], encoding_prefs)
                if best_torrent:
                    selected_torrents.append(best_torrent)
            
            all_torrents = selected_torrents
            logging.info(f"📋 Selected {len(all_torrents)} torrents from {len(albums)} albums")
        
        # Apply filters
        if format_filter:
            all_torrents = [t for t in all_torrents if format_filter.upper() in t.get('format', '').upper()]
        
        if max_downloads:
            all_torrents = all_torrents[:max_downloads]
        
        # Download torrents
        successful = 0
        failed = 0
        
        for i, torrent in enumerate(all_torrents, 1):
            try:
                filename = f"{torrent['torrent_id']}.torrent"
                filepath = output_path / filename
                
                # Download torrent file
                success = await self._download_torrent_file(torrent['torrent_id'], filepath)
                if success:
                    successful += 1
                    logging.info(f"✅ {i}/{len(all_torrents)}: Downloaded {filename}")
                else:
                    failed += 1
                    logging.error(f"❌ {i}/{len(all_torrents)}: Failed {filename}")
                
                # Rate limiting delay
                await asyncio.sleep(delay)
                
            except Exception as e:
                failed += 1
                logging.error(f"❌ {i}/{len(all_torrents)}: Exception - {e}")
        
        return {
            "success": True,
            "collage_name": collage_name,
            "output_directory": str(output_path),
            "total_torrents": len(all_torrents),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(all_torrents)) * 100 if all_torrents else 0,
            "encoding_preferences": encoding_prefs
        }

    async def _download_torrent_file(self, torrent_id: int, filepath: Path) -> bool:
        """Download individual torrent file"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusCollageDownloader/1.0'
        }
        params = {
            'action': 'download',
            'id': torrent_id
        }
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    content = await response.read()
                    filepath.write_bytes(content)
                    return True
        except Exception as e:
            logging.error(f"Download failed for torrent {torrent_id}: {e}")
        
        return False

    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem"""
        return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()
