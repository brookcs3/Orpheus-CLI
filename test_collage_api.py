#!/usr/bin/env python3
"""
Test collage API response to see what data is actually returned
"""

import asyncio
import json
import aiohttp
import ssl

async def test_collage_api():
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
        print(f"📥 Testing collage #{collage_id} (Sampled by The Prodigy)...")
        
        params = {
            'action': 'collage',
            'id': collage_id,
            'page': 1
        }
        
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                if data.get('status') == 'success':
                    resp = data['response']
                    
                    print(f"\n✅ Got response for collage #{collage_id}")
                    print(f"   Name: {resp.get('name')}")
                    print(f"   Category: {resp.get('collageCategoryName')}")
                    
                    # Check what keys are in the response
                    print(f"\n📋 Response keys: {list(resp.keys())}")
                    
                    # Check for torrent groups
                    if 'torrentgroups' in resp:
                        groups = resp['torrentgroups']
                        print(f"\n✅ Found 'torrentgroups' field with {len(groups)} entries")
                        
                        if groups:
                            # Show first few groups
                            print("\n📀 First 3 albums in collage:")
                            for i, group in enumerate(groups[:3], 1):
                                print(f"\n   {i}. Group ID: {group.get('groupId')}")
                                print(f"      Artist: {group.get('artist', 'Unknown')}")
                                print(f"      Album: {group.get('groupName', 'Unknown')}")
                                print(f"      Year: {group.get('groupYear', 'Unknown')}")
                                
                                # Show all keys in a group
                                if i == 1:
                                    print(f"      All keys in group: {list(group.keys())}")
                        else:
                            print("   ⚠️  torrentgroups field is empty!")
                    else:
                        print("\n❌ No 'torrentgroups' field in response")
                    
                    # Check for torrent group ID list
                    if 'torrentGroupIDList' in resp:
                        id_list = resp['torrentGroupIDList']
                        print(f"\n📋 Found 'torrentGroupIDList' with {len(id_list)} IDs")
                        print(f"   First 10 IDs: {id_list[:10]}")
                    
                    # Save full response
                    with open('/Users/cameronbrooks/.orpheus/collage_6936_response.json', 'w') as f:
                        json.dump(data, f, indent=2)
                    print("\n💾 Full response saved to collage_6936_response.json")
                    
                    # Test page 2 if there are multiple pages
                    if resp.get('pages', 1) > 1:
                        print(f"\n📥 Testing page 2...")
                        params['page'] = 2
                        
                        async with session.get(url, params=params, headers=headers) as response2:
                            if response2.status == 200:
                                data2 = await response2.json()
                                if data2.get('status') == 'success':
                                    resp2 = data2['response']
                                    groups2 = resp2.get('torrentgroups', [])
                                    print(f"   Page 2 has {len(groups2)} torrentgroups")
                else:
                    print(f"❌ API error: {data}")
            else:
                print(f"❌ HTTP error: {response.status}")

if __name__ == "__main__":
    asyncio.run(test_collage_api())
