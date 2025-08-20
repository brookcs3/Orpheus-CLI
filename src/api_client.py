#!/usr/bin/env python3
"""
Orpheus API Client - Standard API operations
Handles regular Orpheus API calls as documented in the API docs
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
    Standard Orpheus API client for regular API operations
    Based on the official API documentation
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

    async def _api_request(self, action: str, params: Dict = None) -> Optional[Dict]:
        """Make authenticated API request"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusAPIClient/1.0'
        }
        
        request_params = {'action': action}
        if params:
            request_params.update(params)
        
        try:
            async with self.session.get(url, params=request_params, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('status') == 'success':
                        return data['response']
                    else:
                        logging.error(f"API error: {data}")
                else:
                    logging.error(f"HTTP error: {response.status}")
        except Exception as e:
            logging.error(f"API request failed: {e}")
        
        return None

    async def get_user_info(self) -> Optional[Dict]:
        """Get current user information (index endpoint)"""
        return await self._api_request('index')

    async def get_collage_info(self, collage_id: int, page: int = 1) -> Optional[Dict]:
        """Get collage information"""
        return await self._api_request('collage', {'id': collage_id, 'page': page})

    async def search_torrents(self, search_term: str, page: int = 1, **filters) -> Optional[Dict]:
        """
        Search torrents using browse endpoint
        
        Args:
            search_term: Search string
            page: Page number
            **filters: Additional search filters (format, encoding, etc.)
        """
        params = {
            'searchstr': search_term,
            'page': page
        }
        params.update(filters)
        
        return await self._api_request('browse', params)

    async def get_torrent_group(self, group_id: int) -> Optional[Dict]:
        """Get torrent group details"""
        return await self._api_request('torrentgroup', {'id': group_id})

    async def get_torrent_info(self, torrent_id: int) -> Optional[Dict]:
        """Get individual torrent details"""
        return await self._api_request('torrent', {'id': torrent_id})

    async def get_artist_info(self, artist_id: int = None, artist_name: str = None) -> Optional[Dict]:
        """Get artist information"""
        params = {}
        if artist_id:
            params['id'] = artist_id
        if artist_name:
            params['artistname'] = artist_name
            
        return await self._api_request('artist', params)

    async def search_requests(self, search_term: str = None, page: int = 1, **filters) -> Optional[Dict]:
        """
        Search requests
        
        Args:
            search_term: Search string
            page: Page number
            **filters: Additional filters (tags, show_filled, etc.)
        """
        params = {'page': page}
        if search_term:
            params['search'] = search_term
        params.update(filters)
        
        return await self._api_request('requests', params)

    async def search_users(self, search_term: str, page: int = 1) -> Optional[Dict]:
        """Search users"""
        return await self._api_request('usersearch', {
            'search': search_term,
            'page': page
        })

    async def get_top10(self, top_type: str = 'torrents', details: str = 'all', limit: int = 10) -> Optional[Dict]:
        """
        Get top 10 lists
        
        Args:
            top_type: torrents, users, or tags
            details: Specific category (day, week, month, etc.)
            limit: Number of results (10, 100, or 250)
        """
        return await self._api_request('top10', {
            'type': top_type,
            'details': details,
            'limit': limit
        })

    async def get_bookmarks(self, bookmark_type: str = 'torrents') -> Optional[Dict]:
        """Get user bookmarks"""
        return await self._api_request('bookmarks', {'type': bookmark_type})

    async def get_notifications(self, page: int = 1) -> Optional[Dict]:
        """Get user notifications"""
        return await self._api_request('notifications', {'page': page})

    async def get_announcements(self) -> Optional[Dict]:
        """Get site announcements"""
        return await self._api_request('announcements')

    async def get_subscriptions(self, show_unread: bool = True) -> Optional[Dict]:
        """Get forum subscriptions"""
        return await self._api_request('subscriptions', {
            'showunread': 1 if show_unread else 0
        })

    async def get_request_info(self, request_id: int, page: int = None) -> Optional[Dict]:
        """Get request details"""
        params = {'id': request_id}
        if page:
            params['page'] = page
            
        return await self._api_request('request', params)

    async def search_artists(self, search_term: str, page: int = 1) -> List[Dict]:
        """
        Search for artists (uses torrent search and extracts artists)
        Note: Orpheus doesn't have a dedicated artist search endpoint
        """
        torrent_results = await self.search_torrents(search_term, page=page)
        
        if not torrent_results:
            return []
        
        artists = []
        seen_artists = set()
        
        for result in torrent_results.get('results', []):
            artist_name = result.get('artist', '').strip()
            if artist_name and artist_name not in seen_artists:
                artists.append({
                    'name': artist_name,
                    'group_count': 1,  # We'd need more API calls to get accurate count
                    'sample_albums': [result.get('groupName', '')]
                })
                seen_artists.add(artist_name)
        
        return artists

    async def download_torrent(self, torrent_id: int, use_token: bool = False, 
                             output_path: Path = None) -> bool:
        """
        Download torrent file
        
        Args:
            torrent_id: Torrent ID to download
            use_token: Use FL token for download
            output_path: Where to save the .torrent file
            
        Returns:
            True if successful, False otherwise
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
                        # Successfully got torrent file
                        content = await response.read()
                        
                        if output_path:
                            output_path.write_bytes(content)
                        
                        return True
                    else:
                        # Probably got JSON error response
                        try:
                            error_data = await response.json()
                            logging.error(f"Download failed: {error_data}")
                        except:
                            text = await response.text()
                            logging.error(f"Download failed: {text[:200]}")
                        
                        return False
                else:
                    logging.error(f"Download failed with HTTP {response.status}")
                    return False
                    
        except Exception as e:
            logging.error(f"Download exception: {e}")
            return False

    async def add_torrent_tag(self, group_id: int, tags: List[str]) -> Optional[Dict]:
        """
        Add tags to a torrent group
        
        Args:
            group_id: Torrent group ID
            tags: List of tags to add
            
        Returns:
            API response with added/rejected tags
        """
        tag_string = ','.join(tags)
        
        # This requires POST with authkey, not just API token
        # Would need to implement proper form submission
        logging.warning("add_torrent_tag requires POST with authkey - not implemented")
        return None

    async def get_similar_artists(self, artist_id: int, limit: int = 15) -> Optional[List[Dict]]:
        """Get similar artists"""
        return await self._api_request('similar_artists', {
            'id': artist_id,
            'limit': limit
        })

    async def logchecker(self, log_content: str) -> Optional[Dict]:
        """
        Check ripping log quality
        
        Args:
            log_content: Log file content as string
            
        Returns:
            Log analysis results
        """
        # This requires POST request
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusAPIClient/1.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'action': 'logchecker',
            'pastelog': log_content
        }
        
        try:
            async with self.session.post(url, headers=headers, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('status') == 'success':
                        return result['response']
        except Exception as e:
            logging.error(f"Logchecker failed: {e}")
            
        return None
