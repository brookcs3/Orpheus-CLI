#!/usr/bin/env python3
"""Check if artist API endpoint returns collage membership"""

import asyncio
import json
import aiohttp
import ssl

async def test_artist_api():
    api_key = "PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Test artist endpoint - let's check The Prodigy
        url = "https://orpheus.network/ajax.php"
        
        # First search for The Prodigy to get their artist ID
        search_params = {'action': 'browse', 'artistname': 'The Prodigy'}
        headers = {
            'Authorization': f'token {api_key}',
            'User-Agent': 'Test/1.0'
        }
        
        print("1. Searching for The Prodigy to get artist ID...")
        async with session.get(url, params=search_params, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                if data['response'].get('results'):
                    # Extract artist ID from first result
                    first_result = data['response']['results'][0]
                    print(f"   Found: {first_result}")
                    
                    # Now try to get artist details using artist endpoint
                    # We need to find the actual artist ID
                    # Let's try artist ID 1615 (common for The Prodigy)
                    artist_params = {'action': 'artist', 'id': 1615}
                    
                    print("\n2. Getting artist details for The Prodigy (ID: 1615)...")
                    async with session.get(url, params=artist_params, headers=headers) as artist_response:
                        if artist_response.status == 200:
                            artist_data = await artist_response.json()
                            
                            # Print all keys to see what's available
                            print("\n📋 Keys in artist response:")
                            if 'response' in artist_data:
                                print(list(artist_data['response'].keys()))
                                
                            # Check for collage references
                            response_str = json.dumps(artist_data)
                            if 'collage' in response_str.lower():
                                print("\n✅ Found 'collage' in artist response!")
                                # Print the relevant section
                                for key, value in artist_data['response'].items():
                                    if 'collage' in str(key).lower():
                                        print(f"   {key}: {value}")
                            else:
                                print("\n❌ No 'collage' field in artist response")
                            
                            # Let's also check for Ultramagnetic MC's
                            print("\n3. Checking Ultramagnetic MC's (artist ID: 23817)...")
                            artist_params2 = {'action': 'artist', 'id': 23817}
                            
                            async with session.get(url, params=artist_params2, headers=headers) as artist_response2:
                                if artist_response2.status == 200:
                                    artist_data2 = await artist_response2.json()
                                    
                                    print("\n📋 Keys in Ultramagnetic MC's response:")
                                    if 'response' in artist_data2:
                                        print(list(artist_data2['response'].keys()))
                                        
                                    # Print sample of the response
                                    print("\nSample response structure:")
                                    print(json.dumps(artist_data2['response'], indent=2)[:1000] + "...")

asyncio.run(test_artist_api())
