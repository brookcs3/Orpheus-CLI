#!/usr/bin/env python3
"""
Debug version of the download script to see what's happening
"""

import asyncio
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download_collage_torrents import OrpheusCollageDownloader

async def debug_download():
    async with OrpheusCollageDownloader() as downloader:
        collage_id = 6936
        
        print("🔍 Step 1: Getting collage info...")
        collage_info = await downloader.get_collage_info(collage_id)
        print(f"   Result: {collage_info is not None}")
        if collage_info:
            print(f"   Name: {collage_info.get('name')}")
        
        print("\n🎵 Step 2: Getting all torrents...")
        
        # Manually debug the pagination
        url = f"{downloader.base_url}/ajax.php"
        headers = {
            'Authorization': f'token {downloader.api_key}',
            'User-Agent': 'CollageDownloader/1.0'
        }
        
        page = 1
        params = {
            'action': 'collage',
            'id': collage_id,
            'page': page
        }
        
        print(f"   Making request: {url}")
        print(f"   Params: {params}")
        print(f"   Headers: {headers}")
        
        async with downloader.session.get(url, params=params, headers=headers) as response:
            print(f"   Response status: {response.status}")
            
            if response.status == 200:
                data = await response.json()
                print(f"   Response status field: {data.get('status')}")
                
                if data.get('status') == 'success':
                    resp = data['response']
                    torrentgroups = resp.get('torrentgroups', [])
                    print(f"   Number of torrentgroups: {len(torrentgroups)}")
                    
                    if torrentgroups:
                        first_item = torrentgroups[0]
                        print(f"   First item keys: {list(first_item.keys())}")
                        print(f"   First item has 'group': {'group' in first_item}")
                        print(f"   First item has 'torrents': {'torrents' in first_item}")
                        
                        if 'group' in first_item:
                            group = first_item['group']
                            print(f"   Group keys: {list(group.keys())}")
                            print(f"   Group name: {group.get('name')}")
                        
                        if 'torrents' in first_item:
                            torrents = first_item['torrents']
                            print(f"   Number of torrents in first item: {len(torrents)}")
                else:
                    print(f"   API error: {data}")
            else:
                text = await response.text()
                print(f"   HTTP error: {text[:200]}")

if __name__ == "__main__":
    asyncio.run(debug_download())
