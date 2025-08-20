#!/usr/bin/env python3
"""Test script to get full group details and check for collage info"""

import asyncio
import json
import aiohttp
import ssl

async def get_group_details(group_id):
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    # Disable SSL verification
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        url = "https://orpheus.network/ajax.php"
        params = {
            'action': 'torrentgroup',
            'id': group_id
        }
        headers = {
            'Authorization': f'token {api_key}',
            'User-Agent': 'OrpheusTest/1.0'
        }
        
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f"Error: HTTP {response.status}")
                return None

async def main():
    print("Getting full details for Ultramagnetic MC's - Critical Beatdown (Group ID: 54306)")
    print("-" * 80)
    
    result = await get_group_details(