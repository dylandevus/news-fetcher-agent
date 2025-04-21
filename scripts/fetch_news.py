#!/usr/bin/env python3

# This script loops through a list of sources (Hacker News and various Reddit subreddits) and calls the main function
# from src.main to fetch top posts from each source.
# Usage: $ python3 scripts/fetch_news.py --loop --interval 1

import asyncio
import sys
import os
import argparse
import time
import datetime
from pathlib import Path

# Add the parent directory to sys.path to be able to import from src
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.main import main as main_func

# define an array to hold the fetch arguments
fetch_args = ["Hacker News", "Reddit sub [reactjs]", "Reddit sub [Python]", "Reddit sub [ArtificialInteligence]", "Reddit sub [ChatGPTPro]", "Reddit sub [LocalLLaMA]", "Reddit sub [cybersecurity]", "Reddit sub [netsec]"]

def parse_args():
    parser = argparse.ArgumentParser(description="Fetch top posts from Hacker News or Reddit")
    parser.add_argument(
        "--fetch", 
        type=str,
        help="Source to fetch from: 'Hacker News' or 'Reddit sub NAME' (e.g., 'Reddit sub [reactjs]')",
        default=None
    )
    parser.add_argument(
        "--loop",
        action="store_true",
        help="Run the script in a loop for all sources every 10 minutes"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Interval in minutes between fetching cycles (default: 10)"
    )
    return parser.parse_args()

def set_fetch_arg(fetch_source):
    # Set the fetch_arg in the main module
    import src.main
    src.main.fetch_arg = fetch_source
    
    # Check if fetch_source is the correct attribute - we need to modify it directly
    # to ensure the prompt in main.py is correctly updated
    if hasattr(src.main, 'fetch_arg'):
        # This updates the variable that's used in the f-string for the prompt
        src.main.fetch_arg = fetch_source
    else:
        print("Warning: Could not find fetch_arg in src.main module")
    
    return fetch_source

async def fetch_from_source(source):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{current_time}] Fetching from: {source}")
    try:
        # Pass the source directly to the main function
        await main_func(source=source)
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Completed fetching from: {source}")
    except Exception as e:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Error while fetching from {source}: {str(e)}")
        raise

async def run_once(source):
    await fetch_from_source(source)

async def run_loop(interval_minutes):
    interval_seconds = interval_minutes * 60
    
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Starting fetch cycle")
        
        # Process each source one by one with delay between them
        for idx, source in enumerate(fetch_args):
            try:
                # Process current source
                await fetch_from_source(source)
                
                # If this isn't the last source, wait for the interval before next source
                if idx < len(fetch_args) - 1:
                    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    next_run = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
                    next_run_str = next_run.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{current_time}] Waiting {interval_minutes} minutes before fetching next source. Next fetch at: {next_run_str}")
                    await asyncio.sleep(interval_seconds)
            except Exception as e:
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{current_time}] Error fetching from {source}: {str(e)}")
                # Still wait before next source even if there's an error
                if idx < len(fetch_args) - 1:
                    await asyncio.sleep(interval_seconds)
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Fetch cycle completed. Now running fetch_comments.py to update post comments...")
        
        # Import and run the fetch_comments.py script
        try:
            from scripts.fetch_comments import fetch_and_update_comments
            await fetch_and_update_comments()
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Comment fetching completed.")
        except Exception as e:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{current_time}] Error running fetch_comments.py: {str(e)}")
        
        # Continue with the next cycle after waiting
        next_cycle = datetime.datetime.now() + datetime.timedelta(seconds=interval_seconds)
        next_cycle_str = next_cycle.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}] Next news fetch cycle at {next_cycle_str}")
        await asyncio.sleep(interval_seconds)

async def run():
    args = parse_args()
    
    if args.loop:
        print(f"Running in loop mode with {args.interval} minute interval")
        await run_loop(args.interval)
    elif args.fetch:
        await run_once(args.fetch)
    else:
        print("Please specify either --fetch SOURCE or --loop")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nScript terminated by user")
        sys.exit(0)
