# Youkugrabber

## Instructions:

1. Add the URLs of the videos you want to download into the `urls.py` file. They will be downloaded one by one.

2. If the video is password protected, add all the passwords you may need into the `passwords.py` file.

3. Run `main.py` and wait until the app is done downloading all the videos.

## Notes:

- You can change the download output location from `main.py` by modifying the `output_directory` variable. But that's still a bit wonky.

## Required Libraries:

```bash
pip install yt-dlp
pip install requests
pip install beautifulsoup4
