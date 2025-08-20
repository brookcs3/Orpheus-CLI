#!/usr/bin/env python3
"""
Orpheus API Client - Accurate search implementation
Based exactly on the official API documentation
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path
from typing import Dict, List, Optional
import logging


class OrpheusTorrentSearcher:
    """
    Torrent search using the official Orpheus browse API endpoint
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

    async def search_torrents_api(self, 
                                  searchstr: str = None,
                                  artistname: str = None, 
                                  groupname: str = None,
                                  page: int = 1,
                                  **filters) -> Optional[Dict]:
        """
        Official Orpheus browse API search
        
        From API docs: ajax.php?action=browse&searchstr=<Search Term>
        
        Args:
            searchstr: Free-form search string (searches across multiple fields)
            artistname: Specific artist name filter  
            groupname: Specific album/group name filter
            page: Page number
            **filters: Additional API filters (format, encoding, year, etc.)
            
        Returns:
            API response with torrent groups and torrents
        """
        
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusTorrentSearcher/1.0'
        }
        
        params = {'action': 'browse', 'page': page}
        
        # Add search parameters based on what's provided
        if searchstr:
            params['searchstr'] = searchstr
        if artistname:
            params['artistname'] = artistname  
        if groupname:
            params['groupname'] = groupname
            
        # Add any additional filters
        params.update(filters)
        
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
                    else:
                        logging.error(f"API error: {data}")
                else:
                    logging.error(f"HTTP error: {response.status}")
        except Exception as e:
            logging.error(f"Search failed: {e}")
            
        return None

    async def search_with_encoding_prefs(self, 
                                        query: str,
                                        preferred_encoding: str,
                                        fallback_strategy: str,
                                        limit: int = 50) -> Dict:
        """
        Search torrents and organize by encoding preferences
        
        Args:
            query: Search query (will be used as searchstr in browse API)
            preferred_encoding: User's preferred encoding
            fallback_strategy: "highest" or "lowest" quality fallback
            limit: Maximum results
            
        Returns:
            Organized results with preferred and fallback torrents
        """
        
        # Search using the browse API with searchstr
        api_results = await self.search_torrents_api(searchstr=query)
        
        if not api_results:
            return {
                "error": "No search results",
                "query": query,
                "api_endpoint": "browse",
                "api_parameter": "searchstr"
            }
        
        # Process results and organize by encoding
        preferred_torrents = []
        fallback_torrents = []
        all_torrents = []
        encoding_counts = {}
        
        for group in api_results.get('results', []):
            group_info = {
                'group_id': group.get('groupId'),
                'artist': group.get('artist', 'Unknown Artist'),
                'album': group.get('groupName', 'Unknown Album'), 
                'year': group.get('groupYear', 0),
                'tags': group.get('tags', []),
                'torrents': []
            }
            
            for torrent in group.get('torrents', []):
                torrent_info = {
                    'torrent_id': torrent.get('torrentId'),
                    'group_id': group_info['group_id'],
                    'artist': group_info['artist'],
                    'album': group_info['album'],
                    'year': group_info['year'],
                    'format': torrent.get('format', ''),
                    'encoding': torrent.get('encoding', ''),
                    'media': torrent.get('media', ''),
                    'hasLog': torrent.get('hasLog', False),
                    'logScore': torrent.get('logScore', 0),
                    'hasCue': torrent.get('hasCue', False),
                    'seeders': torrent.get('seeders', 0),
                    'leechers': torrent.get('leechers', 0),
                    'snatches': torrent.get('snatches', 0),
                    'size': torrent.get('size', 0),
                    'scene': torrent.get('scene', False)
                }
                
                # Count encodings
                encoding = torrent_info['encoding']
                encoding_counts[encoding] = encoding_counts.get(encoding, 0) + 1
                
                # Categorize by preference
                if self._matches_preferred_encoding(torrent_info, preferred_encoding):
                    preferred_torrents.append(torrent_info)
                else:
                    fallback_torrents.append(torrent_info)
                    
                all_torrents.append(torrent_info)
                group_info['torrents'].append(torrent_info)
        
        # Sort fallback torrents by quality strategy
        if fallback_strategy == "highest":
            fallback_torrents.sort(key=self._get_quality_score, reverse=True)
        else:  # "lowest"
            fallback_torrents.sort(key=self._get_quality_score, reverse=False)
        
        return {
            "success": True,
            "query": query,
            "search_method": {
                "api_endpoint": "ajax.php?action=browse",
                "parameter_used": "searchstr",
                "note": "Free-form search across torrent database fields"
            },
            "encoding_analysis": {
                "preferred_encoding": preferred_encoding,
                "preferred_matches": len(preferred_torrents),
                "fallback_available": len(fallback_torrents),
                "fallback_strategy": fallback_strategy,
                "all_encodings_found": encoding_counts
            },
            "results": {
                "preferred_torrents": preferred_torrents[:limit//2],
                "fallback_torrents": fallback_torrents[:limit//2], 
                "all_torrents": all_torrents[:limit]
            }
        }

    async def analyze_available_encodings(self, query: str) -> Dict:
        """
        Analyze what encodings are available for a search query
        Helps users choose appropriate preferred_encoding
        """
        
        api_results = await self.search_torrents_api(searchstr=query)
        
        if not api_results:
            return {"error": "No search results for analysis"}
        
        format_encoding_combos = {}
        quality_levels = {}
        
        for group in api_results.get('results', []):
            for torrent in group.get('torrents', []):
                format_str = torrent.get('format', 'Unknown')
                encoding_str = torrent.get('encoding', 'Unknown')
                combo = f"{format_str} {encoding_str}"
                
                # Count combinations
                format_encoding_combos[combo] = format_encoding_combos.get(combo, 0) + 1
                
                # Analyze quality
                quality_score = self._get_quality_score({
                    'format': format_str,
                    'encoding': encoding_str,
                    'hasLog': torrent.get('hasLog', False),
                    'logScore': torrent.get('logScore', 0),
                    'hasCue': torrent.get('hasCue', False)
                })
                
                quality_levels[combo] = max(quality_levels.get(combo, 0), quality_score)
        
        # Sort by popularity and quality
        sorted_by_count = sorted(format_encoding_combos.items(), key=lambda x: x[1], reverse=True)
        sorted_by_quality = sorted(quality_levels.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "query": query,
            "total_torrents": sum(format_encoding_combos.values()),
            "available_encodings": {
                "by_popularity": sorted_by_count[:10],  # Top 10 most common
                "by_quality": sorted_by_quality[:10]    # Top 10 highest quality
            },
            "recommendations": {
                "most_common": sorted_by_count[0][0] if sorted_by_count else "None found",
                "highest_quality": sorted_by_quality[0][0] if sorted_by_quality else "None found",
                "suggested_preferences": [item[0] for item in sorted_by_count[:5]]
            }
        }

    def _matches_preferred_encoding(self, torrent: Dict, preferred_encoding: str) -> bool:
        """Check if torrent matches user's preferred encoding"""
        format_str = torrent.get('format', '').lower()
        encoding_str = torrent.get('encoding', '').lower()
        preferred = preferred_encoding.lower().strip()
        
        # Direct matches
        if preferred in encoding_str or preferred in format_str:
            return True
            
        # Common patterns
        patterns = {
            '320': format_str == 'mp3' and '320' in encoding_str,
            'v0': format_str == 'mp3' and 'v0' in encoding_str,
            'v1': format_str == 'mp3' and 'v1' in encoding_str, 
            'v2': format_str == 'mp3' and 'v2' in encoding_str,
            'flac': format_str == 'flac',
            'lossless': 'lossless' in encoding_str,
            '24bit': '24bit' in encoding_str
        }
        
        return patterns.get(preferred, False)

    def _get_quality_score(self, torrent: Dict) -> int:
        """Assign quality score for sorting fallback options"""
        format_str = torrent.get('format', '').upper()
        encoding_str = torrent.get('encoding', '').upper()
        has_log = torrent.get('hasLog', False)
        log_score = torrent.get('logScore', 0)
        has_cue = torrent.get('hasCue', False)
        
        # Base format scores
        format_scores = {
            'FLAC': 100,
            'MP3': 80, 
            'AAC': 60,
            'OGG': 40
        }
        
        # Encoding scores
        encoding_scores = {
            '24BIT LOSSLESS': 95,
            'LOSSLESS': 90,
            '320': 85,
            'V0 (VBR)': 83,
            'V1 (VBR)': 80,
            '256': 75,
            'V2 (VBR)': 70,
            '192': 60,
            '128': 40
        }
        
        base_score = format_scores.get(format_str, 30)
        encoding_bonus = encoding_scores.get(encoding_str, 20)
        
        # Quality bonuses
        quality_bonus = 0
        if has_log and log_score == 100:
            quality_bonus += 10
        elif has_log:
            quality_bonus += 5
        if has_cue:
            quality_bonus += 3
            
        return base_score + encoding_bonus + quality_bonus

    async def download_with_smart_selection(self, 
                                          torrent_ids: List[int] = None,
                                          search_results: Dict = None,
                                          preferred_encoding: str = None,
                                          fallback_strategy: str = None,
                                          output_dir: str = None,
                                          max_downloads: int = None,
                                          delay: float = 2.0,
                                          dry_run: bool = False) -> Dict:
        """Download torrents with smart encoding selection"""
        
        # Implementation for downloading selected torrents
        # This would use the download API endpoint
        
        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "message": "Dry run - no actual downloads performed",
                "would_download": {
                    "torrent_ids": torrent_ids or [],
                    "encoding_preferences": {
                        "preferred": preferred_encoding,
                        "fallback_strategy": fallback_strategy
                    }
                }
            }
        
        # Actual download implementation would go here
        return {"error": "Download implementation needed"}
