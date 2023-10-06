import json
import os

import whisper
from pytube import YouTube, exceptions

videos = [f for f in os.listdir("failed/transcripts_disabled")]

all_data = []
for video in videos:
    with open(f"failed/transcripts_disabled/{video}") as _file:
        data = json.load(_file)

    video_id = data["videoId"]
    if os.path.isfile(f"staging_data/{video}"):
        continue

    print(f"Downloading video {video_id}")
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        audio_file = (
            YouTube(video_url)
            .streams.filter(only_audio=True)
            .first()
            .download(filename=f"/tmp/{video_id}.mp4")
        )
    # KeyError: 'content-length'
    except KeyError:
        print(f"Failed obtaining audio for {video_id} (KeyError)")
        continue
    # kZB-Up9HnT4 is age restricted, and can't be accessed without logging in.
    except exceptions.AgeRestrictedError:
        print(f"Failed obtaining audio for {video_id} (AgeRestrictedError)")
        continue
    # jys_9oreLA0 is a private video
    except exceptions.VideoPrivate:
        print(f"Failed obtaining audio for {video_id} (VideoPrivate)")
        continue

    print(f"Transcribing video {video_id}")
    whisper_model = whisper.load_model("medium")
    # TODO: Try tweaking the patience and bean_size, eg. patience=2, beam_size=5
    transcription = whisper_model.transcribe(audio_file, language="es")

    with open(f"staging_data/{video_id}.json", "w") as _file:
        json.dump(transcription, _file, indent=4)
