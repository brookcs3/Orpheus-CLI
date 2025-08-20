#!/usr/bin/env python3
"""
Test if album/torrent group details include collage membership
Testing with: Ultramagnetic MC's - Critical Beatdown (1988)
"""

import asyncio
import json
import aiohttp
import ssl

async def test_album_collages():
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
        
        # Step 1: Search for the album
        print("🔍 Step 1: Searching for 'Ultramagnetic MC's - Critical Beatdown'...")
        search_params = {
            'action': 'browse',
            'artistname': 'Ultramagnetic',
            'groupname': 'Critical Beatdown',
            'year': '1988'
        }
        
        async with session.get(url, params=search_params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                if data.get('status') == 'success' and data['response'].get('results'):
                    results = data['response']['results']
                    print(f"   Found {len(results)} result(s)")
                    
                    # Find the right album
                    target_group = None
                    for result in results:
                        if 'Critical Beatdown' in result.get('groupName', ''):
                            target_group = result
                            print(f"\n✅ Found the album!")
                            print(f"   Artist: {result.get('artist')}")
                            print(f"   Album: {result.get('groupName')}")
                            print(f"   Year: {result.get('groupYear')}")
                            print(f"   Group ID: {result.get('groupId')}")
                            break
                    
                    if not target_group:
                        print("❌ Couldn't find Critical Beatdown in results")
                        return
                    
                    group_id = target_group.get('groupId')
                    
                    # Step 2: Get full torrent group details
                    print(f"\n🔍 Step 2: Fetching torrent group details (ID: {group_id})...")
                    group_params = {
                        'action': 'torrentgroup',
                        'id': group_id
                    }
                    
                    async with session.get(url, params=group_params, headers=headers) as group_response:
                        if group_response.status == 200:
                            group_data = await group_response.json()
                            
                            if group_data.get('status') == 'success':
                                response_data = group_data['response']
                                
                                # Check all keys for collage references
                                print("\n📋 Keys in torrentgroup response:")
                                print(list(response_data.keys()))
                                
                                # Check if 'collages' field exists
                                if 'collages' in response_data:
                                    print("\n✅ FOUND 'collages' field in response!")
                                    collages = response_data['collages']
                                    print(f"   This album is in {len(collages)} collage(s):")
                                    for collage in collages:
                                        print(f"   - ID: {collage.get('id')} - {collage.get('name')}")
                                else:
                                    # Search for any mention of collage in the response
                                    response_str = json.dumps(response_data).lower()
                                    if 'collage' in response_str:
                                        print("\n⚠️  'collage' mentioned somewhere in response (but not as a field)")
                                        # Try to find where
                                        for key, value in response_data.items():
                                            if 'collage' in str(value).lower():
                                                print(f"   Found in '{key}': {str(value)[:200]}")
                                    else:
                                        print("\n❌ No 'collages' field or mention in torrentgroup response")
                                
                                # Let's also check the structure of the response
                                print("\n📄 Response structure (first level):")
                                for key in response_data.keys():
                                    value_type = type(response_data[key]).__name__
                                    if isinstance(response_data[key], (list, dict)):
                                        if isinstance(response_data[key], list):
                                            print(f"   {key}: list with {len(response_data[key])} items")
                                        else:
                                            print(f"   {key}: dict with keys: {list(response_data[key].keys())[:5]}")
                                    else:
                                        print(f"   {key}: {value_type}")
                                
                                # Save full response for inspection
                                with open('/Users/cameronbrooks/.orpheus/critical_beatdown_response.json', 'w') as f:
                                    json.dump(group_data, f, indent=2)
                                print("\n💾 Full response saved to critical_beatdown_response.json")
                                
                else:
                    print(f"❌ Search failed: {data}")
            else:
                print(f"❌ HTTP error: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_album_collages())
