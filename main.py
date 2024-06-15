import os
import re
import requests
from bs4 import BeautifulSoup
import yt_dlp as youtube_dl
from urls import video_urls

def sanitize_youku_url(video_url):
    # Remove anything after '==.html'
    return re.sub(r'(==\.html).*', r'\1', video_url)

def get_video_title(video_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(video_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title_tag = soup.find('meta', property='og:title')
    if title_tag:
        return title_tag['content']
    else:
        return None

def get_next_filename(output_directory, base_filename):
    # Check if base_filename already exists in output_directory
    filename = base_filename
    counter = 0
    while os.path.exists(os.path.join(output_directory, f"{filename}.mp4")):
        counter += 1
        filename = f"{base_filename}_{counter}"
    return f"{filename}.mp4"

def download_video(video_url, output_directory, passwords):
    video_url = sanitize_youku_url(video_url)  # Sanitize the video URL
    video_title = get_video_title(video_url)
    if video_title:
        base_filename = video_title
    else:
        base_filename = "downloaded_video"
    
    output_filename = get_next_filename(output_directory, base_filename)

    ydl_opts = {
        'outtmpl': os.path.join(output_directory, output_filename),
        'format': 'best'
    }

    for password in passwords:
        try:
            print(f"Trying password: {password}")
            ydl_opts['videopassword'] = password
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print("Download successful!")
            return True  # Exit the function if download is successful
        except youtube_dl.utils.DownloadError as e:
            print(f"Download failed with password: {password}, trying next password...")
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print(f"All passwords failed. Unable to download the video {video_url}.")
    return False

def main():
    output_directory = 'downloaded_videos'
    passwords = ['zmack', 'footnotes']  # Replace these with actual passwords, not all videos have the same password
    
    for index, video_url in enumerate(video_urls, start=1):
        print(f"Downloading video {index} of {len(video_urls)}: {video_url}")
        success = download_video(video_url, output_directory, passwords)
        if not success:
            print(f"Failed to download video {index}: {video_url}")
    
    print("All videos downloaded!")

if __name__ == "__main__":
    main()
