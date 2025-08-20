#!/usr/bin/env python3
"""
Test specifically the get_collage_info function
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from download_collage_torrents import OrpheusCollageDownloader

async def test_collage_info():
    async with OrpheusCollageDownloader() as downloader:
        print("🔍 Testing get_collage_info function...")
        
        # Test the exact function that's failing
        collage_info = await downloader.get_collage_info(6936)
        
        if collage_info:
            print("✅ get_collage_info SUCCESS")
            print(f"   Name: {collage_info.get('name')}")
            print(f"   Category: {collage_info.get('collageCategoryName')}")
            print(f"   Groups: {len(collage_info.get('torrentGroupIDList', []))}")
        else:
            print("❌ get_collage_info FAILED - returned None")
            
        # Test get_all_collage_torrents 
        print("\n🎵 Testing get_all_collage_torrents...")
        try:
            all_torrents = await downloader.get_all_collage_torrents(6936)
            print(f"✅ Found {len(all_torrents)} torrents")
            if all_torrents:
                print(f"   First torrent: {all_torrents[0].get('artist')} - {all_torrents[0].get('album')}")
        except Exception as e:
            print(f"❌ get_all_collage_torrents failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_collage_info())
