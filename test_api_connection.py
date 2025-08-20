#!/usr/bin/env python3
"""
Test API connection to debug the issue
"""

import asyncio
import json
import aiohttp
import ssl
from pathlib import Path

async def test_api():
    # Load API key
    config_path = Path.home() / '.orpheus' / 'config.json'
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = json.load(f)
            api_key = config.get('api_key', 'PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C')
    else:
        api_key = 'PSTi7lCo1E4Q9IHgYJvVg3zVpBBUOpGEaer0t1l26Eg5bw1J7l88wk2ua1IGs8X8bCFMej8DFA4Kfb/lMzl3TdWIhx7d50KW6oYTcOEw8Ed7gDLcI6+C'
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        base_url = "https://orpheus.network"
        headers = {
            'Authorization': f'token {api_key}',
            'User-Agent': 'APITest/1.0'
        }
        
        print("🔐 Testing API connection...")
        print(f"📍 Base URL: {base_url}")
        print(f"🔑 API Key: {api_key[:20]}...")
        
        # Test 1: Basic API endpoint
        print("\n📡 Test 1: Basic API call...")
        try:
            url = f"{base_url}/ajax.php"
            params = {'action': 'index'}
            
            async with session.get(url, params=params, headers=headers) as response:
                print(f"   Status: {response.status}")
                print(f"   Headers: {dict(response.headers)}")
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        print(f"   Response: {json.dumps(data, indent=2)[:500]}...")
                    except:
                        text = await response.text()
                        print(f"   Text Response: {text[:500]}...")
                else:
                    text = await response.text()
                    print(f"   Error Response: {text[:500]}...")
                    
        except Exception as e:
            print(f"   ❌ Exception: {e}")
        
        # Test 2: Collage API call
        print("\n📚 Test 2: Collage API call...")
        try:
            url = f"{base_url}/ajax.php"
            params = {
                'action': 'collage',
                'id': 6936,
                'page': 1
            }
            
            async with session.get(url, params=params, headers=headers) as response:
                print(f"   Status: {response.status}")
                
                if response.status == 200:
                    try:
                        data = await response.json()
                        if data.get('status') == 'success':
                            resp = data['response']
                            print(f"   ✅ Success! Collage: {resp.get('name')}")
                            print(f"   📊 Total groups: {len(resp.get('torrentGroupIDList', []))}")
                        else:
                            print(f"   ❌ API Error: {data}")
                    except Exception as parse_e:
                        text = await response.text()
                        print(f"   ❌ Parse Error: {parse_e}")
                        print(f"   Raw Response: {text[:300]}...")
                else:
                    text = await response.text()
                    print(f"   ❌ HTTP Error: {text[:300]}...")
                    
        except Exception as e:
            print(f"   ❌ Request Exception: {e}")
        
        # Test 3: Website connectivity
        print("\n🌐 Test 3: Website connectivity...")
        try:
            async with session.get(f"{base_url}/", allow_redirects=True) as response:
                print(f"   Website Status: {response.status}")
                if response.status == 200:
                    text = await response.text()
                    if 'orpheus' in text.lower():
                        print("   ✅ Website accessible")
                    else:
                        print("   ⚠️  Unexpected website content")
                        print(f"   Content sample: {text[:200]}...")
                else:
                    print(f"   ❌ Website not accessible: {response.status}")
        except Exception as e:
            print(f"   ❌ Website test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())
