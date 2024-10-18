import datetime
import json
import os
import xml

import requests
import scrapetube
from aws_lambda_powertools import Logger
from timelength import TimeLength
from youtube_transcript_api import YouTubeTranscriptApi, _errors

AMLO_CHANNEL_ID = "UCxEgOKuI-n-WOJaNcisHvSg"
SHEINBAUM_CHANNEL_ID = "UCvzHrtf9by1-UY67SfZse8w"

logger = Logger()


def handler(channel_id):
    # Get a list of all playlists in the channel
    api_key = os.environ["YOUTUBE_V3_API_KEY"]
    playlists = requests.get(
        "https://www.googleapis.com/youtube/v3/playlists",
        params={
            "part": "snippet",
            "channelId": channel_id,
            "key": api_key,
            "maxResults": 50,
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

    # Check if video has already been processed
    for path in ["data", "failed"]:
        local_path = f"{path}/{video_id}.json"
        if os.path.isfile(local_path):
            logger.info("File already exists", extra={"local_path": local_path})
            return

    # Retrieve or generate transcriptions
    failed_path = f"failed/{video_id}.json"
    logger.info("Obtaining transcriptions", extra={"video_id": video_id})
    try:
        transcription_with_timestamps = YouTubeTranscriptApi.get_transcript(
            video_id, languages=["es"]
        )
    except _errors.TranscriptsDisabled:
        logger.warning("Transcripts are disabled", extra={"video_id": video_id})
        with open(failed_path, "w") as _file:
            json.dump(video_metadata, _file, indent=4)
        return
    # See https://github.com/jdepoix/youtube-transcript-api/issues/320
    except xml.etree.ElementTree.ParseError:
        logger.warning("Retrieving transcript failed", extra={"video_id": video_id})
        return
    # Language for some videos is not Spanish - ES
    # Example: https://www.youtube.com/watch?v=k_rBgKb1y8U
    except _errors.NoTranscriptFound:
        logger.warning("No transcript available", extra={"video_id": video_id})
        with open(failed_path, "w") as _file:
            json.dump(video_metadata, _file, indent=4)
        return

    transcription_text = ""
    for part in transcription_with_timestamps:
        transcription_text += f" {part['text']} "
    transcription_text = transcription_text.replace("  ", " ")
    transcription_text = transcription_text.strip()

    if not video_metadata.get("videoInfo"):
        published_time_text = video_metadata["publishedTimeText"]["simpleText"]
        video_length = video_metadata["lengthText"]["accessibility"]["accessibilityData"]["label"]
        video_length_seconds = TimeLength(video_length)
        assert video_length_seconds.result.success
        video_length_seconds = video_length_seconds.result.seconds
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
        "retrieved_time": str(datetime.datetime.now(datetime.timezone.utc)),
    }
    with open(local_path, "w") as _file:
        json.dump(video, _file, indent=4)

    return video


if __name__ == "__main__":
    if os.getenv("AMLO"):
        channel_id = AMLO_CHANNEL_ID
    else:
        channel_id = SHEINBAUM_CHANNEL_ID
    handler(channel_id)
