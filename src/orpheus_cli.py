#!/usr/bin/env python3
"""
Orpheus Collage Tools - Comprehensive CLI
Discover, search, and download music from Orpheus collages with intelligent preferences.
"""

import asyncio
import click
import json
import sys
from pathlib import Path
from typing import List, Optional

# Import our core modules
from .core.collage_discoverer import CollageDiscoverer  
from .core.database_builder import DatabaseBuilder
from .core.torrent_downloader import TorrentDownloader
from .core.config_manager import ConfigManager


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """🎵 Orpheus Collage Tools - Discover and download music intelligently"""
    if ctx.invoked_subcommand is None:
        click.echo("🎵 Orpheus Collage Tools Suite")
        click.echo("=" * 35)
        click.echo()
        ctx.get_help()


# =============================================================================
# DISCOVERY COMMANDS
# =============================================================================

@cli.group()
def discover():
    """🔍 Discover albums and collages"""
    pass


@discover.command("album")
@click.option("--artist", help="Artist name to search for")  
@click.option("--album", help="Album name to search for")
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json", "csv"]),
              help="Output format")
@click.option("--limit", default=50, help="Maximum results to return")
async def discover_album(artist: str, album: str, output_format: str, limit: int):
    """Find which collages contain a specific album"""
    async with CollageDiscoverer() as discoverer:
        results = await discoverer.find_album_in_collages(
            artist=artist, album=album, limit=limit
        )
        
        if output_format == "json":
            click.echo(json.dumps(results, indent=2))
        elif output_format == "csv":
            # CSV output logic
            pass
        else:
            # Table output (default)
            if results:
                click.echo(f"✅ Found {len(results)} collage(s) containing {artist} - {album}")
                for i, collage in enumerate(results, 1):
                    click.echo(f"{i:2d}. [{collage['id']:>5}] {collage['name']}")
            else:
                click.echo("❌ No collages found")


@discover.command("artist")  
@click.argument("artist_name")
@click.option("--limit", default=100, help="Maximum albums to return")
@click.option("--format", "output_format", default="table", type=click.Choice(["table", "json"]))
async def discover_artist(artist_name: str, limit: int, output_format: str):
    """Find all albums by an artist and their collage memberships"""
    async with CollageDiscoverer() as discoverer:
        results = await discoverer.find_artist_albums(artist_name, limit=limit)
        
        if output_format == "json":
            click.echo(json.dumps(results, indent=2))
        else:
            click.echo(f"🎤 Artist: {artist_name}")
            click.echo(f"📀 Found {len(results)} album(s)")
            
            for album in results:
                collage_count = len(album.get('collages', []))
                status = "📚 In collages" if collage_count > 0 else "📝 Not in collages" 
                click.echo(f"  • {album['name']} ({album['year']}) - {status}: {collage_count}")


# =============================================================================  
# DATABASE COMMANDS
# =============================================================================

@cli.group()
def database():
    """📊 Database operations for offline search"""
    pass


@database.command("build")
@click.option("--output", default="./collage_database", help="Output directory")
@click.option("--force", is_flag=True, help="Rebuild even if database exists")
@click.option("--parallel", default=4, help="Number of parallel workers")
async def build_database(output: str, force: bool, parallel: int):
    """Build complete offline collage database (30+ minutes)"""
    click.echo("🏗️ Building complete collage database...")
    click.echo("⚠️  This will take 30+ minutes")
    
    if not force and Path(output).exists():
        if not click.confirm("Database exists. Rebuild?"):
            return
    
    async with DatabaseBuilder() as builder:
        progress_callback = lambda current, total: click.echo(f"📊 Progress: {current}/{total} collages processed")
        
        await builder.build_complete_database(
            output_dir=output,
            parallel_workers=parallel,
            progress_callback=progress_callback
        )
    
    click.echo("✅ Database build complete!")


@database.command("stats")
@click.option("--database", default="./collage_database", help="Database directory")
def database_stats(database: str):
    """Show database statistics"""
    db_path = Path(database)
    if not db_path.exists():
        click.echo("❌ Database not found. Run 'database build' first.")
        return
        
    # Load and show stats
    stats_file = db_path / "stats.json"
    if stats_file.exists():
        with open(stats_file) as f:
            stats = json.load(f)
        
        click.echo("📊 Database Statistics")
        click.echo("=" * 25)
        click.echo(f"📚 Total collages: {stats.get('total_collages', 'Unknown'):,}")
        click.echo(f"💿 Total albums: {stats.get('total_albums', 'Unknown'):,}")
        click.echo(f"🎵 Total torrents: {stats.get('total_torrents', 'Unknown'):,}")
        click.echo(f"📅 Last updated: {stats.get('last_updated', 'Unknown')}")
    else:
        click.echo("📊 Database found but no statistics available")


@database.command("search")
@click.option("--artist", help="Search by artist name")
@click.option("--album", help="Search by album name") 
@click.option("--database", default="./collage_database", help="Database directory")
@click.option("--limit", default=20, help="Maximum results")
async def search_database(artist: str, album: str, database: str, limit: int):
    """Search the offline database"""
    if not artist and not album:
        click.echo("❌ Must specify --artist or --album")
        return
        
    db_path = Path(database)
    if not db_path.exists():
        click.echo("❌ Database not found. Run 'database build' first.")
        return
    
    async with DatabaseBuilder() as builder:
        results = await builder.search_database(
            database_path=database,
            artist=artist,
            album=album,
            limit=limit
        )
        
        if results:
            click.echo(f"🔍 Found {len(results)} result(s)")
            for result in results:
                collages = result.get('collages', [])
                click.echo(f"🎵 {result['artist']} - {result['album']} ({result['year']})")
                if collages:
                    click.echo(f"   📚 In {len(collages)} collage(s):")
                    for collage in collages[:3]:  # Show first 3
                        click.echo(f"     • [{collage['id']}] {collage['name']}")
                    if len(collages) > 3:
                        click.echo(f"     • ... and {len(collages) - 3} more")
                else:
                    click.echo("   📝 Not in any collages")
                click.echo()
        else:
            click.echo("❌ No results found")


# =============================================================================
# DOWNLOAD COMMANDS  
# =============================================================================

@cli.group()
def download():
    """⬇️ Download torrents from collages"""
    pass


@download.command("collage")
@click.argument("collage_id", type=int)
@click.option("--output", help="Output directory")
@click.option("--prefer-320", is_flag=True, help="Prefer 320 CBR MP3 (default)")
@click.option("--prefer-flac", is_flag=True, help="Prefer FLAC with logs")
@click.option("--prefer-v0", is_flag=True, help="Prefer V0 VBR MP3")
@click.option("--encoding-priority", multiple=True, help="Custom encoding priority")
@click.option("--format-filter", help="Filter by format (FLAC, MP3, etc.)")
@click.option("--max", "max_downloads", type=int, help="Maximum torrents to download")
@click.option("--all-versions", is_flag=True, help="Download all versions (not just best per album)")
@click.option("--delay", default=2.0, type=float, help="Delay between downloads (seconds)")
@click.option("--use-tokens", is_flag=True, help="Use FL tokens for downloads")
@click.option("--dry-run", is_flag=True, help="Show what would be downloaded without downloading")
async def download_collage(
    collage_id: int, output: str, prefer_320: bool, prefer_flac: bool, prefer_v0: bool,
    encoding_priority: List[str], format_filter: str, max_downloads: int, 
    all_versions: bool, delay: float, use_tokens: bool, dry_run: bool
):
    """Download torrents from a collage with intelligent encoding preferences"""
    
    # Build encoding preferences
    if encoding_priority:
        prefs = list(encoding_priority)
    elif prefer_flac:
        prefs = ['FLAC Log 100', 'FLAC Log', 'FLAC Lossless', 'FLAC', '320', 'V0']
    elif prefer_v0:
        prefs = ['V0', '320', 'FLAC Lossless', 'FLAC']
    else:  # Default or prefer_320
        prefs = ['320', 'FLAC Lossless', 'FLAC Log 100', 'FLAC Log', 'FLAC', 'V0']
    
    click.echo(f"🎯 Downloading collage #{collage_id}")
    click.echo(f"🎵 Encoding preferences: {' → '.join(prefs)}")