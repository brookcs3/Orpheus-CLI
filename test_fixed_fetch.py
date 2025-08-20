#!/usr/bin/env python3
"""
Quick test to verify the fix works for fetching collage contents
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path

async def test_fixed_fetch():
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        url = "https://orpheus.network/ajax.php"
        headers = {
            'Authorization': f'token {api_key}',
            'User-Agent': 'Test/1.0'
        }
        
        # Test with collage 6936 (Sampled by The Prodigy)
        collage_id = 6936
        all_albums = []
        page = 1
        
        print(f"📥 Fetching collage #{collage_id} with fixed parsing...")
        
        while True:
            params = {
                'action': 'collage',
                'id': collage_id,
                'page': page
            }
            
            async with session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    break
                
                data = await response.json()
                if data.get('status') != 'success':
                    break
                
                resp = data['response']
                
                # Get album/artist info from this page
                for item in resp.get('torrentgroups', []):
                    # The actual group info is nested inside 'group'
                    group = item.get('group', {})
                    
                    # Extract artist names from musicInfo
                    artists = []
                    music_info = group.get('musicInfo', {})
                    if music_info:
                        # Get main artists
                        for artist in music_info.get('artists', []):
                            artists.append(artist.get('name', ''))
                        # Also get 'with' artists if any
                        for artist in music_info.get('with', []):
                            artists.append(artist.get('name', ''))
                    
                    artist_str = ', '.join(artists) if artists else 'Various Artists'
                    
                    album_entry = {
                        'album_id': group.get('id'),
                        'album_name': group.get('name', ''),
                        'artist': artist_str,
                        'year': group.get('year', '')
                    }
                    all_albums.append(album_entry)
                
                print(f"   Page {page}: Found {len(resp.get('torrentgroups', []))} albums")
                
                # Check if more pages
                if page >= resp.get('pages', 1):
                    break
                page += 1
        
        print(f"\n✅ Total albums found: {len(all_albums)}")
        
        # Show first few albums
        print("\n📀 First 5 albums in collage:")
        for i, album in enumerate(all_albums[:5], 1):
            print(f"\n   {i}. Album ID: {album['album_id']}")
            print(f"      Artist: {album['artist']}")
            print(f"      Album: {album['album_name']}")
            print(f"      Year: {album['year']}")
        
        # Check for Ultramagnetic MC's
        print("\n🔍 Checking for Ultramagnetic MC's...")
        for album in all_albums:
            if 'Ultramagnetic' in album['artist']:
                print(f"   ✅ Found: {album['artist']} - {album['album_name']} ({album['year']})")

if __name__ == "__main__":
    asyncio.run(test_fixed_fetch())
