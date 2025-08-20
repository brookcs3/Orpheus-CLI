#!/usr/bin/env python3
"""
Database Builder for Offline Collage Search
Creates and manages the complete collage database for fast searching
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path
from typing import Dict, List, Optional, Callable
import logging
from datetime import datetime


class CollageDatabase:
    """
    Build and manage offline collage database for fast searching
    """
    
    def __init__(self, database_path: str = "./collage_database"):
        self.database_path = Path(database_path)
        config_path = Path.home() / '.orpheus' / 'config.json'
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.api_key = config.get('api_key')
        else:
            self.api_key = None
            
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

    async def build_complete_database(self, output_dir: str = None, force: bool = False,
                                    parallel_workers: int = 4, 
                                    progress_callback: Callable = None) -> Dict:
        """
        Build complete collage database by fetching all collages
        This takes 30+ minutes but enables instant offline searches
        """
        
        if output_dir:
            self.database_path = Path(output_dir)
        
        if self.database_path.exists() and not force:
            return {"error": "Database exists. Use force=True to rebuild"}
            
        self.database_path.mkdir(parents=True, exist_ok=True)
        
        logging.info("🏗️ Building complete collage database...")
        logging.info("⚠️ This will take 30+ minutes")
        
        # First, get list of all collages
        all_collages = await self._get_all_collage_ids()
        total_collages = len(all_collages)
        
        logging.info(f"📊 Found {total_collages} collages to process")
        
        # Process collages in parallel batches
        processed = 0
        complete_database = {
            'collages': {},
            'albums': {},
            'artists': {},
            'metadata': {
                'total_collages': total_collages,
                'build_date': datetime.now().isoformat(),
                'version': '1.0'
            }
        }
        
        # Process in batches
        batch_size = parallel_workers * 10
        for i in range(0, total_collages, batch_size):
            batch = all_collages[i:i + batch_size]
            
            # Process batch in parallel
            semaphore = asyncio.Semaphore(parallel_workers)
            tasks = []
            
            for collage_id in batch:
                task = self._process_collage_with_semaphore(semaphore, collage_id)
                tasks.append(task)
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Add successful results to database
            for result in batch_results:
                if isinstance(result, dict) and 'collage_id' in result:
                    self._add_collage_to_database(complete_database, result)
                    processed += 1
                    
                    if progress_callback:
                        progress_callback(processed, total_collages)
            
            # Save progress periodically
            if processed % 100 == 0:
                await self._save_database_chunk(complete_database, processed)
        
        # Final save
        await self._save_complete_database(complete_database)
        
        stats = {
            'total_collages': total_collages,
            'processed': processed,
            'total_albums': len(complete_database['albums']),
            'total_artists': len(complete_database['artists']),
            'build_completed': datetime.now().isoformat()
        }
        
        # Save statistics
        stats_file = self.database_path / 'stats.json'
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2)
        
        logging.info(f"✅ Database build complete! Processed {processed}/{total_collages} collages")
        return stats

    async def _get_all_collage_ids(self) -> List[int]:
        """Get list of all collage IDs by browsing collage pages"""
        all_collage_ids = []
        
        # Browse collages by category to get all IDs
        categories = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # Common collage category IDs
        
        for category in categories:
            page = 1
            while True:
                url = f"{self.base_url}/collages.php"
                params = {
                    'type': category,
                    'page': page
                }
                
                try:
                    async with self.session.get(url, params=params) as response:
                        if response.status != 200:
                            break
                            
                        html = await response.text()
                        
                        # Extract collage IDs from HTML
                        import re
                        collage_ids = re.findall(r'collages\.php\?id=(\d+)', html)
                        
                        if not collage_ids:
                            break
                            
                        for collage_id in collage_ids:
                            if int(collage_id) not in all_collage_ids:
                                all_collage_ids.append(int(collage_id))
                        
                        page += 1
                        
                        # Stop if we've seen this pattern before (last page)
                        if len(set(collage_ids)) < 5:
                            break
                            
                except Exception as e:
                    logging.error(f"Failed to get collages for category {category}, page {page}: {e}")
                    break
        
        return sorted(list(set(all_collage_ids)))

    async def _process_collage_with_semaphore(self, semaphore: asyncio.Semaphore, collage_id: int) -> Dict:
        """Process single collage with semaphore for rate limiting"""
        async with semaphore:
            return await self._process_single_collage(collage_id)

    async def _process_single_collage(self, collage_id: int) -> Dict:
        """Process a single collage and extract all its data"""
        url = f"{self.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {self.api_key}',
            'User-Agent': 'OrpheusCollageDatabase/1.0'
        }
        
        all_torrents = []
        page = 1
        
        # Get all pages of the collage
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
                    
                    # Store collage metadata on first page
                    if page == 1:
                        collage_info = {
                            'collage_id': collage_id,
                            'name': resp.get('name', ''),
                            'description': resp.get('description_raw', ''),
                            'category': resp.get('collageCategoryName', ''),
                            'creator_id': resp.get('creatorID', 0),
                            'total_groups': len(resp.get('torrentGroupIDList', [])),
                            'albums': []
                        }
                    
                    # Process torrent groups
                    torrentgroups = resp.get('torrentgroups', [])
                    if not torrentgroups:
                        break
                    
                    for item in torrentgroups:
                        group = item.get('group', {})
                        torrents = item.get('torrents', [])
                        
                        # Extract artist info
                        artists = []
                        music_info = group.get('musicInfo', {})
                        if music_info:
                            for artist in music_info.get('artists', []):
                                artists.append(artist.get('name', ''))
                        
                        artist_str = ', '.join(artists) if artists else 'Unknown Artist'
                        
                        album_info = {
                            'group_id': group.get('id'),
                            'artist': artist_str,
                            'album': group.get('name', ''),
                            'year': group.get('year', 0),
                            'torrents': []
                        }
                        
                        # Add torrent details
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
                                'size': torrent.get('size', 0)
                            }
                            album_info['torrents'].append(torrent_info)
                        
                        collage_info['albums'].append(album_info)
                    
                    if page >= resp.get('pages', 1):
                        break
                    
                    page += 1
                    
                    # Small delay to be respectful
                    await asyncio.sleep(0.1)
                    
            except Exception as e:
                logging.error(f"Failed to process collage {collage_id}, page {page}: {e}")
                break
        
        return collage_info

    def _add_collage_to_database(self, database: Dict, collage_data: Dict):
        """Add collage data to the main database structure"""
        collage_id = collage_data['collage_id']
        database['collages'][collage_id] = collage_data
        
        # Index albums and artists for fast searching
        for album in collage_data.get('albums', []):
            group_id = album['group_id']
            artist = album['artist'].lower()
            album_name = album['album'].lower()
            
            # Add to albums index
            if group_id not in database['albums']:
                database['albums'][group_id] = {
                    'artist': album['artist'],
                    'album': album['album'],
                    'year': album['year'],
                    'collages': []
                }
            
            database['albums'][group_id]['collages'].append({
                'id': collage_id,
                'name': collage_data['name']
            })
            
            # Add to artists index
            if artist not in database['artists']:
                database['artists'][artist] = {
                    'name': album['artist'],
                    'albums': []
                }
            
            if group_id not in [a['group_id'] for a in database['artists'][artist]['albums']]:
                database['artists'][artist]['albums'].append({
                    'group_id': group_id,
                    'album': album['album'],
                    'year': album['year']
                })

    async def _save_database_chunk(self, database: Dict, processed: int):
        """Save database progress"""
        chunk_file = self.database_path / f'progress_{processed}.json'
        with open(chunk_file, 'w') as f:
            json.dump({
                'processed': processed,
                'total_collages': len(database['collages']),
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)

    async def _save_complete_database(self, database: Dict):
        """Save the complete database"""
        main_file = self.database_path / 'complete_collage_database.json'
        with open(main_file, 'w') as f:
            json.dump(database, f, indent=2)
        
        logging.info(f"💾 Database saved to {main_file}")

    async def search(self, artist: str = None, album: str = None, limit: int = 20) -> List[Dict]:
        """Search the offline database"""
        database_file = self.database_path / 'complete_collage_database.json'
        
        if not database_file.exists():
            raise Exception("Database not found. Run build_complete_database() first.")
        
        with open(database_file, 'r') as f:
            database = json.load(f)
        
        results = []
        
        if artist:
            artist_key = artist.lower()
            # Partial matching for artists
            matching_artists = [k for k in database['artists'].keys() if artist_key in k]
            
            for artist_key in matching_artists[:limit]:
                artist_data = database['artists'][artist_key]
                for album_info in artist_data['albums']:
                    group_id = album_info['group_id']
                    if str(group_id) in database['albums']:
                        album_data = database['albums'][str(group_id)]
                        results.append({
                            'artist': artist_data['name'],
                            'album': album_info['album'],  
                            'year': album_info['year'],
                            'group_id': group_id,
                            'collages': album_data['collages']
                        })
        
        elif album:
            album_key = album.lower()
            # Search through all albums
            for group_id, album_data in database['albums'].items():
                if album_key in album_data['album'].lower():
                    results.append({
                        'artist': album_data['artist'],
                        'album': album_data['album'],
                        'year': album_data['year'],
                        'group_id': int(group_id),
                        'collages': album_data['collages']
                    })
                    
                    if len(results) >= limit:
                        break
        
        return results[:limit]

    async def get_stats(self) -> Dict:
        """Get database statistics"""
        stats_file = self.database_path / 'stats.json'
        
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                return json.load(f)
        else:
            return {"error": "Database statistics not found"}
