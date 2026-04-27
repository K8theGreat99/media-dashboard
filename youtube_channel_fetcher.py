import requests
import json
import time
import csv

# YouTube API Configuration
API_KEY = "YOUR_API_KEY_HERE"
SEARCH_ENDPOINT = "https://www.googleapis.com/youtube/v3/search"
CHANNELS_ENDPOINT = "https://www.googleapis.com/youtube/v3/channels"

# List of channel names to search for
CHANNEL_NAMES = [
    "Caroline Winkler",
    "Christy Ann Jones",
    "Sparrows End",
    "Anna Howard",
    "Snapdragon Life",
    "Rajiv Surendra",
    "Bernadette Banner",
    "Esoterica",
    "Kaz Rowe",
    "V Birchwood",
    "Nicole Rudolph",
    "Miniminuteman",
    "More Perfect Union",
    "Cozy Creative",
    "Theo - t3.gg",
    "Matt Wolfe",
    "Wes Roth",
    "AI Revolution",
    "Endeavorance",
    "Phillip DeFranco",
    "Under the Desk News",
    "Legal Eagle",
    "The Daily Show",
    "The Late Show with Stephen Colbert",
    "Ryan Hall Y'all",
    "Fall of Civilizations",
    "Cambrian Chronicles",
    "Dan Davis History",
    "Rita Wilkins",
    "Decoding the Unknown",
    "Crashing Out with Philip DeFranco & Alex Pearlman"
]

def search_channel(channel_name):
    """Search for a YouTube channel by name and return results."""
    params = {
        'part': 'snippet',
        'type': 'channel',
        'q': channel_name,
        'key': API_KEY,
        'maxResults': 5  # Get top 5 results to help with matching
    }
    
    try:
        response = requests.get(SEARCH_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error searching for '{channel_name}': {e}")
        return None

def get_channel_details(channel_id):
    """Get detailed information about a channel including subscriber count."""
    params = {
        'part': 'snippet,statistics',
        'id': channel_id,
        'key': API_KEY
    }
    
    try:
        response = requests.get(CHANNELS_ENDPOINT, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('items'):
            return data['items'][0]
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting details for channel {channel_id}: {e}")
        return None

def process_channels():
    """Process all channels and return results."""
    results = []
    
    for i, channel_name in enumerate(CHANNEL_NAMES, 1):
        print(f"Processing {i}/{len(CHANNEL_NAMES)}: {channel_name}")
        
        # Search for the channel
        search_results = search_channel(channel_name)
        
        if not search_results or 'items' not in search_results:
            results.append({
                'input_name': channel_name,
                'channel_id': 'NOT FOUND',
                'channel_title': '',
                'custom_url': '',
                'subscriber_count': '',
                'status': 'ERROR - No results found'
            })
            time.sleep(0.5)  # Brief pause to avoid rate limits
            continue
        
        items = search_results['items']
        
        if len(items) == 0:
            results.append({
                'input_name': channel_name,
                'channel_id': 'NOT FOUND',
                'channel_title': '',
                'custom_url': '',
                'subscriber_count': '',
                'status': 'No matching channels found'
            })
        elif len(items) == 1:
            # Only one result - likely correct
            channel_id = items[0]['id']['channelId']
            details = get_channel_details(channel_id)
            
            if details:
                snippet = details.get('snippet', {})
                stats = details.get('statistics', {})
                
                results.append({
                    'input_name': channel_name,
                    'channel_id': channel_id,
                    'channel_title': snippet.get('title', ''),
                    'custom_url': snippet.get('customUrl', ''),
                    'subscriber_count': stats.get('subscriberCount', 'Hidden'),
                    'status': 'OK - Single match'
                })
        else:
            # Multiple results - flag for manual review
            channel_id = items[0]['id']['channelId']
            details = get_channel_details(channel_id)
            
            if details:
                snippet = details.get('snippet', {})
                stats = details.get('statistics', {})
                
                # Show info about other matches
                other_matches = []
                for item in items[1:3]:  # Show up to 2 alternative matches
                    other_matches.append(item['snippet']['title'])
                
                status = f"⚠️ VERIFY - {len(items)} matches found. Top result selected. Others: {', '.join(other_matches)}"
                
                results.append({
                    'input_name': channel_name,
                    'channel_id': channel_id,
                    'channel_title': snippet.get('title', ''),
                    'custom_url': snippet.get('customUrl', ''),
                    'subscriber_count': stats.get('subscriberCount', 'Hidden'),
                    'status': status
                })
        
        # Pause between requests to be respectful of API limits
        time.sleep(0.5)
    
    return results

def save_results(results):
    """Save results to a CSV file."""
    output_file = 'youtube_channel_ids.csv'
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['input_name', 'channel_id', 'channel_title', 'custom_url', 'subscriber_count', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n✅ Results saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    print("Starting YouTube Channel ID extraction...")
    print(f"Processing {len(CHANNEL_NAMES)} channels\n")
    
    results = process_channels()
    output_file = save_results(results)
    
    # Print summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    verified_count = sum(1 for r in results if 'OK' in r['status'])
    needs_review_count = sum(1 for r in results if '⚠️' in r['status'])
    error_count = sum(1 for r in results if 'ERROR' in r['status'] or 'NOT FOUND' in r['channel_id'])
    
    print(f"✅ Confirmed matches: {verified_count}")
    print(f"⚠️  Need manual review: {needs_review_count}")
    print(f"❌ Errors/Not found: {error_count}")
    print(f"\nTotal processed: {len(results)}")
