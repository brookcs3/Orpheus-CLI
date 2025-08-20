#!/usr/bin/env python3
"""Check if torrentgroup API returns any collage info (even if undocumented)"""

import asyncio
import json
import aiohttp
import ssl

async def test_api():
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Test torrentgroup endpoint
        url = "https://orpheus.network/ajax.php"
        params = {'action': 'torrentgroup', 'id': 54306}  # Ultramagnetic MC's
        headers = {
            'Authorization': f'token {api_key}',
            'User-Agent': 'Test/1.0'
        }
        
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                
                # Pretty print the entire response to see ALL fields
                print("Full torrentgroup response for Ultramagnetic MC's - Critical Beatdown:")
                print("=" * 80)
                print(json.dumps(data, indent=2))
                print("=" * 80)
                
                # Check for any collage-related fields
                response_str = json.dumps(data)
                if 'collage' in response_str.lower():
                    print("\n✅ Found 'collage' in response!")
                else:
                    print("\n❌ No 'collage' field found in response")
                    
                print("\n📋 Top-level keys in response:")
                if 'response' in data:
                    print(list(data['response'].keys()))
                    if 'group' in data['response']:
                        print("\n📋 Keys in 'group':")
                        print(list(data['response']['group'].keys()))

asyncio.run(test_api())
