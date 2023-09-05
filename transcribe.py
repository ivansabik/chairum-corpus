import json
import os.path
from os import listdir
from os.path import isfile, join

from youtube_transcript_api import YouTubeTranscriptApi, _errors

videos = [f for f in listdir("data/videos") if isfile(join("data/videos", f))]

for video in videos:
    if os.path.isfile(f"data/transcriptions_raw/{video}"):
        continue
    video_id = video.replace(".json", "")
    try:
        transcription = YouTubeTranscriptApi.get_transcript(video_id, languages=["es"])
    except _errors.TranscriptsDisabled as e:
        print(e)
        continue
    # Language for some videos is not Spanish - ES
    # Example: https://www.youtube.com/watch?v=k_rBgKb1y8U
    except _errors.NoTranscriptFound as e:
        print(e)
        continue
    with open(f"data/transcriptions_raw/{video_id}.json", "w") as _file:
        json.dump(transcription, _file)
