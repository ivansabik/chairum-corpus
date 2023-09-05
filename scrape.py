import json
import os

import requests
import scrapetube

api_key = os.environ["YOUTUBE_V3_API_KEY"]
channel_id = "UCxEgOKuI-n-WOJaNcisHvSg"
playlists = requests.get(
    "https://www.googleapis.com/youtube/v3/playlists",
    params={
        "part": "snippet",
        "channelId": channel_id,
        "key": api_key,
    },
)
playlists = playlists.json()
playlists = [p["id"] for p in playlists["items"]]

for playlist in playlists:
    videos = scrapetube.get_playlist(playlist)
    for video in videos:
        video_id = video["videoId"]
        with open(f"data/videos/{video_id}.json", "w") as _file:
            json.dump(video, _file)

videos = scrapetube.get_channel(channel_id)
for video in videos:
    video_id = video["videoId"]
    with open(f"data/videos/{video_id}.json", "w") as _file:
        json.dump(video, _file)
