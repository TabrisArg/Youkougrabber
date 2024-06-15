import requests
from bs4 import BeautifulSoup
import re
import time

# Define the output filename variable using Zmack's channel as an example
output_filename = "zmack_channel_urls.py"

def fetch_video_items(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    video_items = []
    offset = 0
    page_size = 20  # Number of videos to fetch per request
    max_videos_to_fetch = 100  # Adjust based on your observation

    try:
        while len(video_items) < max_videos_to_fetch:
            print(f"Fetching videos from offset {offset}...")
            params = {
                'spm': 'a2h0c.8166622.PhoneSokuUgc_2.1',
                'uid': 'UMzQwODcwMTM2',
                'offset': offset,
                'pageSize': page_size
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                new_video_items = extract_video_items(response.text)
                if not new_video_items:
                    print("No more videos found. Exiting.")
                    break
                video_items.extend(new_video_items)
                offset += page_size
                print(f"Fetched {len(new_video_items)} new videos. Total: {len(video_items)} videos.")
                time.sleep(1)  # Add a small delay to avoid hitting server too frequently
            else:
                print(f"Failed to fetch page: {url}. Status code: {response.status_code}")
                break

            # Check if no new videos were fetched in the current request
            if len(new_video_items) == 0:
                print("No more videos available. Exiting.")
                break

            # Limit to max_videos_to_fetch
            if len(video_items) >= max_videos_to_fetch:
                break

    except Exception as e:
        print(f"Exception occurred: {str(e)}")

    return video_items[:max_videos_to_fetch]  # Limit to max_videos_to_fetch

def extract_video_items(html_text):
    video_items = []

    soup = BeautifulSoup(html_text, 'html.parser')
    videos = soup.find_all('a', class_='videoitem_titlelink')

    for video in videos:
        try:
            url = 'https:' + video.get('href', 'No URL found')
            video_items.append(url)
        except Exception as e:
            print(f"Error extracting video information: {str(e)}")

    return video_items

def create_video_urls_file(channel_name, video_urls):
    filename = f"{channel_name}_channel_urls.py"
    with open(filename, 'w') as file:
        file.write(f"video_urls = {video_urls}")

    print(f"File '{filename}' created successfully with {len(video_urls)} video URLs.")

def main():
    global output_filename  # Allow modification of the global variable

    # Extract channel name from output_filename
    channel_name = output_filename.split('_')[0]

    print(f"Channel name: {channel_name}")
    print(f"Fetching videos from: https://www.youku.com/profile/index/")
    video_items = fetch_video_items('https://www.youku.com/profile/index/')

    if video_items:
        print(f"Total {len(video_items)} videos fetched.")
        create_video_urls_file(channel_name, video_items)
    else:
        print("No video items found on the page.")

if __name__ == "__main__":
    main()
