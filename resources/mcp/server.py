from typing import Dict, Any
from src.torrent_searcher import OrpheusTorrentSearcher
from src.collage_discoverer import CollageDiscoverer
from src.torrent_downloader import TorrentDownloader

class MCP:
    def __init__(self):
        self.tools = {}

    def tool(self, func):
        self.tools[func.__name__] = func
        return func

    def resource(self, name):
        def decorator(func):
            # In a real scenario, you would handle resources appropriately
            return func
        return decorator

mcp = MCP()

@mcp.tool()
async def search_and_download(
    preferred_encoding: str,
    fallback_strategy: str,
    searchstr: str = None,
    artistname: str = None,
    groupname: str = None,
    limit: int = 50,
    output_dir: str = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Searches for torrents and downloads them based on encoding preferences.

    Args:
        preferred_encoding: The preferred encoding (e.g., '320', 'V0', 'FLAC').
        fallback_strategy: The fallback strategy ('highest' or 'lowest').
        searchstr: A free-form search string.
        artistname: The artist's name.
        groupname: The album's name.
        limit: The maximum number of results to return.
        output_dir: The directory to save the downloaded files to.
        dry_run: If True, the function will only print what it would do.

    Returns:
        A dictionary containing the results of the operation.
    """
    search_results = await search_torrents(
        preferred_encoding,
        fallback_strategy,
        searchstr,
        artistname,
        groupname,
        limit
    )

    if search_results.get("error"):
        return search_results

    downloader = TorrentDownloader()
    download_results = await downloader.download_torrents(
        search_results["results"]["preferred_torrents"],
        output_dir,
        dry_run=dry_run
    )

    return {
        "search_results": search_results,
        "download_results": download_results,
    }


@mcp.tool()
async def discover_album_in_collages(
    artist: str,
    album: str,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Discovers which collages an album belongs to.

    Args:
        artist: The artist's name.
        album: The album's name.
        limit: The maximum number of results to return.

    Returns:
        A dictionary containing the results of the operation.
    """
    async with CollageDiscoverer() as discoverer:
        results = await discoverer.find_album_in_collages(
            artist=artist, album=album, limit=limit
        )
        return results

from typing import Dict, Any
from src.torrent_searcher import OrpheusTorrentSearcher
from src.collage_discoverer import CollageDiscoverer
from src.torrent_downloader import TorrentDownloader

class MCP:
    def __init__(self):
        self.tools = {}

    def tool(self, func):
        self.tools[func.__name__] = func
        return func

    def resource(self, name):
        def decorator(func):
            # In a real scenario, you would handle resources appropriately
            return func
        return decorator

mcp = MCP()

@mcp.tool()
async def search_and_download(
    preferred_encoding: str,
    fallback_strategy: str,
    searchstr: str = None,
    artistname: str = None,
    groupname: str = None,
    limit: int = 50,
    output_dir: str = None,
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Searches for torrents and downloads them based on encoding preferences.

    Args:
        preferred_encoding: The preferred encoding (e.g., '320', 'V0', 'FLAC').
        fallback_strategy: The fallback strategy ('highest' or 'lowest').
        searchstr: A free-form search string.
        artistname: The artist's name.
        groupname: The album's name.
        limit: The maximum number of results to return.
        output_dir: The directory to save the downloaded files to.
        dry_run: If True, the function will only print what it would do.

    Returns:
        A dictionary containing the results of the operation.
    """
    search_results = await search_torrents(
        preferred_encoding,
        fallback_strategy,
        searchstr,
        artistname,
        groupname,
        limit
    )

    if search_results.get("error"):
        return search_results

    downloader = TorrentDownloader()
    download_results = await downloader.download_torrents(
        search_results["results"]["preferred_torrents"],
        output_dir,
        dry_run=dry_run
    )

    return {
        "search_results": search_results,
        "download_results": download_results,
    }


@mcp.tool()
async def discover_album_in_collages(
    artist: str,
    album: str,
    limit: int = 50
) -> Dict[str, Any]:
    """
    Discovers which collages an album belongs to.

    Args:
        artist: The artist's name.
        album: The album's name.
        limit: The maximum number of results to return.

    Returns:
        A dictionary containing the results of the operation.
    """
    async with CollageDiscoverer() as discoverer:
        results = await discoverer.find_album_in_collages(
            artist=artist, album=album, limit=limit
        )
        return results

@mcp.tool()
async def search_torrents(
    preferred_encoding: str,
    fallback_strategy: str,
    searchstr: str = None,
    artistname: str = None,
    groupname: str = None,
    limit: int = 50
) -> Dict[str, Any]:
    """
    🎵 Search torrents using Orpheus browse API
    
    Based on API docs: ajax.php?action=browse&searchstr=<Search Term>
    
    Args:
        preferred_encoding: REQUIRED - Preferred encoding (320, V0, FLAC, etc.)
        fallback_strategy: REQUIRED - "highest" or "lowest" quality when preferred unavailable
        searchstr: Free-form search string (searches across torrent database fields)
        artistname: Specific artist name filter (more precise than searchstr)
        groupname: Specific album/group name filter (more precise than searchstr)
        limit: Maximum results
        
    Returns:
        Torrents organized by preferred vs fallback encodings
        
    Note: Use either searchstr OR artistname+groupname, not both
    """
    
    if not preferred_encoding:
        return {"error": "preferred_encoding is required (e.g., '320', 'V0', 'FLAC')"}
    
    if fallback_strategy not in ["highest", "lowest"]:
        return {"error": "fallback_strategy must be 'highest' or 'lowest'"}
    
    # Validate search parameters
    if not searchstr and not artistname and not groupname:
        return {"error": "Must specify searchstr OR artistname/groupname"}
    
    if searchstr and (artistname or groupname):
        return {"error": "Use either searchstr OR artistname+groupname, not both"}
    
    try:
        async with OrpheusTorrentSearcher() as searcher:
            if searchstr:
                # Free-form search using searchstr parameter
                results = await searcher.search_with_encoding_prefs(
                    query=searchstr,
                    preferred_encoding=preferred_encoding,
                    fallback_strategy=fallback_strategy,
                    limit=limit
                )
            else:
                # Specific artist/album search using dedicated parameters
                api_results = await searcher.search_torrents_api(
                    artistname=artistname,
                    groupname=groupname
                )
                
                # Process the specific search results
                results = await searcher.process_api_results_with_encoding_prefs(
                    api_results=api_results,
                    preferred_encoding=preferred_encoding,
                    fallback_strategy=fallback_strategy,
                    limit=limit
                )
            
            return {
                "success": True,
                "search_parameters": {
                    "searchstr": searchstr,
                    "artistname": artistname,
                    "groupname": groupname,
                    "api_endpoint": "ajax.php?action=browse"
                },
                "preferred_encoding": preferred_encoding,
                "fallback_strategy": fallback_strategy,
                "results": results
            }
            
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}


@mcp.tool()
async def get_available_encodings(
    searchstr: str = None,
    artistname: str = None,
    groupname: str = None
) -> Dict[str, Any]:
    """
    📊 Preview available encodings for your search
    
    Shows what encodings are actually available so you can choose
    appropriate preferred_encoding parameter.
    
    Args:
        searchstr: Free-form search string (browse API searchstr parameter)
        artistname: Specific artist name (browse API artistname parameter)  
        groupname: Specific album name (browse API groupname parameter)
        
    Returns:
        Available encodings with counts and recommendations
        
    Note: Use either searchstr OR artistname+groupname, not both
    """
    
    if not searchstr and not artistname and not groupname:
        return {"error": "Must specify searchstr OR artistname/groupname"}
    
    if searchstr and (artistname or groupname):
        return {"error": "Use either searchstr OR artistname+groupname, not both"}
    
    try:
        async with OrpheusTorrentSearcher() as searcher:
            if searchstr:
                analysis = await searcher.analyze_available_encodings(searchstr)
                search_method = "Free-form search (searchstr parameter)"
            else:
                # For specific artist/album, we need to build a query
                query_parts = []
                if artistname:
                    query_parts.append(artistname)
                if groupname:
                    query_parts.append(groupname)
                query = " ".join(query_parts)
                
                analysis = await searcher.analyze_available_encodings_specific(
                    artistname=artistname,
                    groupname=groupname
                )
                search_method = f"Specific search (artistname: {artistname}, groupname: {groupname})"
            
            return {
                "success": True,
                "search_parameters": {
                    "searchstr": searchstr,
                    "artistname": artistname, 
                    "groupname": groupname,
                    "search_method": search_method
                },
                "available_encodings": analysis,
                "usage_note": "Choose preferred_encoding from the available options above"
            }
            
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


@mcp.resource("orpheus://api-info")
async def get_api_info() -> str:
    """Information about Orpheus API search capabilities"""
    return """
# Orpheus API Search Methods

## Browse API Endpoint
**URL**: `ajax.php?action=browse`

## Search Parameters (choose ONE approach):

### Method 1: Free-form Search
- **Parameter**: `searchstr` 
- **Usage**: `searchstr="The Prodigy Music for the Jilted Generation"`
- **What it does**: Searches across multiple torrent database fields
- **Best for**: General searches, when you're not sure of exact artist/album names

### Method 2: Specific Fields  
- **Parameters**: `artistname` and/or `groupname`
- **Usage**: `artistname="The Prodigy"` + `groupname="Music for the Jilted Generation"`
- **What it does**: Searches specific database fields
- **Best for**: When you know exact artist and album names

## DO NOT mix methods
- Don't use `searchstr` + `artistname` together
- Use either free-form OR specific fields, not both

## Additional API Filters
The browse endpoint also supports:
- `format` (FLAC, MP3, etc.)
- `encoding` (320, V0, Lossless, etc.)  
- `media` (CD, Vinyl, WEB, etc.)
- `year`, `haslog`, `scene`, etc.

## Examples
```python
# Free-form search
search_torrents(
    preferred_encoding="320",
    fallback_strategy="highest", 
    searchstr="Prodigy Jilted Generation"
)

# Specific search  
search_torrents(
    preferred_encoding="FLAC",
    fallback_strategy="highest",
    artistname="The Prodigy",
    groupname="Music for the Jilted Generation"
)
```
"""


@mcp.tool()
async def get_available_encodings(
    searchstr: str = None,
    artistname: str = None,
    groupname: str = None
) -> Dict[str, Any]:
    """
    📊 Preview available encodings for your search
    
    Shows what encodings are actually available so you can choose
    appropriate preferred_encoding parameter.
    
    Args:
        searchstr: Free-form search string (browse API searchstr parameter)
        artistname: Specific artist name (browse API artistname parameter)  
        groupname: Specific album name (browse API groupname parameter)
        
    Returns:
        Available encodings with counts and recommendations
        
    Note: Use either searchstr OR artistname+groupname, not both
    """
    
    if not searchstr and not artistname and not groupname:
        return {"error": "Must specify searchstr OR artistname/groupname"}
    
    if searchstr and (artistname or groupname):
        return {"error": "Use either searchstr OR artistname+groupname, not both"}
    
    try:
        async with OrpheusTorrentSearcher() as searcher:
            if searchstr:
                analysis = await searcher.analyze_available_encodings(searchstr)
                search_method = "Free-form search (searchstr parameter)"
            else:
                # For specific artist/album, we need to build a query
                query_parts = []
                if artistname:
                    query_parts.append(artistname)
                if groupname:
                    query_parts.append(groupname)
                query = " ".join(query_parts)
                
                analysis = await searcher.analyze_available_encodings_specific(
                    artistname=artistname,
                    groupname=groupname
                )
                search_method = f"Specific search (artistname: {artistname}, groupname: {groupname})"
            
            return {
                "success": True,
                "search_parameters": {
                    "searchstr": searchstr,
                    "artistname": artistname, 
                    "groupname": groupname,
                    "search_method": search_method
                },
                "available_encodings": analysis,
                "usage_note": "Choose preferred_encoding from the available options above"
            }
            
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}


@mcp.resource("orpheus://api-info")
async def get_api_info() -> str:
    """Information about Orpheus API search capabilities"""
    return """
# Orpheus API Search Methods

## Browse API Endpoint
**URL**: `ajax.php?action=browse`

## Search Parameters (choose ONE approach):

### Method 1: Free-form Search
- **Parameter**: `searchstr` 
- **Usage**: `searchstr="The Prodigy Music for the Jilted Generation"`
- **What it does**: Searches across multiple torrent database fields
- **Best for**: General searches, when you're not sure of exact artist/album names

### Method 2: Specific Fields  
- **Parameters**: `artistname` and/or `groupname`
- **Usage**: `artistname="The Prodigy"` + `groupname="Music for the Jilted Generation"`
- **What it does**: Searches specific database fields
- **Best for**: When you know exact artist and album names

## DO NOT mix methods
- Don't use `searchstr` + `artistname` together
- Use either free-form OR specific fields, not both

## Additional API Filters
The browse endpoint also supports:
- `format` (FLAC, MP3, etc.)
- `encoding` (320, V0, Lossless, etc.)  
- `media` (CD, Vinyl, WEB, etc.)
- `year`, `haslog`, `scene`, etc.

## Examples
```python
# Free-form search
search_torrents(
    preferred_encoding="320",
    fallback_strategy="highest", 
    searchstr="Prodigy Jilted Generation"
)

# Specific search  
search_torrents(
    preferred_encoding="FLAC",
    fallback_strategy="highest",
    artistname="The Prodigy",
    groupname="Music for the Jilted Generation"
)
```
"""