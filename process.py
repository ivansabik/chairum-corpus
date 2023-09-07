import datetime
import json
import os
import os.path

import requests
import scrapetube
from timelength import TimeLength
from youtube_transcript_api import YouTubeTranscriptApi, _errors


def handler():
    # Get a list of all playlists in the channel
    api_key = os.environ["YOUTUBE_V3_API_KEY"]
    channel_id = "UCxEgOKuI-n-WOJaNcisHvSg"
    playlists = requests.get(
        "https://www.googleapis.com/youtube/v3/playlists",
        params={
            "part": "snippet",
            "channelId": channel_id,
            "key": api_key,
            "maxResults": 50
        },
    )
    playlists = playlists.json()
    # Make sure there are not more than 50 playlists in the results
    # since pagination has not been implemented
    assert not playlists.get("nextPageToken")

    # Process videos in playlists
    for playlist in playlists["items"]:
        playlist_id = playlist["id"]
        videos = scrapetube.get_playlist(playlist_id)
        for video in videos:
            video["playlist_id"] = playlist_id
            video["playlist_title"] = playlist["snippet"]["title"]
            _process_video(video)

    # Process videos in the channel not part of playlists
    videos = scrapetube.get_channel(channel_id)
    for video in videos:
        video["playlist_id"] = None
        video["playlist_title"] = None
        _process_video(video)


def _process_video(video_metadata):
    video_id = video_metadata["videoId"]
    local_path = f"data/{video_id}.json"
    if os.path.isfile(local_path):
        return

    try:
        transcription_with_timestamps = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["es"]
        )
    except _errors.TranscriptsDisabled as e:
        print(f"Transcripts are disabled for video {video_id}")
        return
    # Language for some videos is not Spanish - ES
    # Example: https://www.youtube.com/watch?v=k_rBgKb1y8U
    except _errors.NoTranscriptFound as e:
        print(f"No transcript available for video {video_id}")
        return

    transcription_text = ""
    for part in transcription_with_timestamps:
        transcription_text += f" {part['text']} "
    transcription_text = transcription_text.replace("  ", " ")

    if not video_metadata.get("videoInfo"):
        published_time_text = video_metadata["publishedTimeText"]["simpleText"]
        video_length = video_metadata["lengthText"]["accessibility"][
            "accessibilityData"
        ]["label"]
        video_length_seconds = TimeLength(video_length).total_seconds
        video_length_seconds = int(video_length_seconds)
    else:
        published_time_text = video_metadata["videoInfo"]["runs"][-1]["text"]
        video_length_seconds = int(video_metadata["lengthSeconds"])

    video = {
        "video_id": video_id,
        "video_thumbnail_url": video_metadata["thumbnail"]["thumbnails"][-1]["url"],
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "video_title": video_metadata["title"]["runs"][-1]["text"],
        "video_length_seconds": video_length_seconds,
        "transcription_with_timestamps": transcription_with_timestamps,
        "transcription_text": transcription_text,
        "transcription_source": "YouTube auto-generated captions",
        "playlist_id": video_metadata["playlist_id"],
        "playlist_title": video_metadata["playlist_title"],
        "published_time_text": published_time_text,
        "retrieved_time": str(datetime.datetime.utcnow()),
    }

    with open(local_path, "w") as _file:
        json.dump(video, _file, indent=4)

    return video


if __name__ == "__main__":
    handler()
