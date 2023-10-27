import datetime
import json
import os

import whisper
from pytube import YouTube, exceptions
from timelength import TimeLength

videos = [f for f in os.listdir("failed")]

all_data = []
for video in videos:
    _video_metadata_file = f"failed/{video}"
    with open(_video_metadata_file) as _file:
        video_metadata = json.load(_file)

    video_id = video_metadata["videoId"]
    if os.path.isfile(f"manual_transcriptions/{video}"):
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
    # EMb7n2q5qSc is streaming live and cannot be loaded
    except exceptions.LiveStreamError:
        print(f"Failed obtaining audio for {video_id} (LiveStreamError)")
        continue
    print(f"Transcribing video {video_id}")
    whisper_model = whisper.load_model("medium")
    # TODO: Try tweaking the patience and bean_size, eg. patience=2, beam_size=5
    transcription = whisper_model.transcribe(audio_file, language="es")

    with open(f"manual_transcriptions/{video_id}.json", "w") as _file:
        json.dump(transcription, _file, indent=4)

    # Create cleaned data
    transcription_with_timestamps = []
    for part in transcription["segments"]:
        if part["no_speech_prob"] < 0.85:
            transcription_with_timestamps.append(
                {
                    "text": part["text"],
                    "start": part["start"],
                    "duration": part["end"] - part["start"],
                }
            )

    transcription_text = ""
    for part in transcription_with_timestamps:
        transcription_text += f"{part['text']} "
    transcription_text = transcription_text.replace("  ", " ")
    transcription_text = transcription_text.strip()

    if not video_metadata.get("videoInfo"):
        published_time_text = video_metadata["publishedTimeText"]["simpleText"]
        video_length = video_metadata["lengthText"]["accessibility"]["accessibilityData"]["label"]
        video_length_seconds = TimeLength(video_length).total_seconds
        video_length_seconds = int(video_length_seconds)
    else:
        published_time_text = video_metadata["videoInfo"]["runs"][-1]["text"]
        if video_metadata.get("lengthSeconds"):
            video_length_seconds = int(video_metadata["lengthSeconds"])
        else:
            print(f"Length not found for video {video_id}")
            video_length_seconds = None

    video = {
        "video_id": video_id,
        "video_thumbnail_url": video_metadata["thumbnail"]["thumbnails"][-1]["url"],
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
        "video_title": video_metadata["title"]["runs"][-1]["text"],
        "video_length_seconds": video_length_seconds,
        "transcription_with_timestamps": transcription_with_timestamps,
        "transcription_text": transcription_text,
        "transcription_source": "Manually transcribed v0.0.1",
        "playlist_id": video_metadata["playlist_id"],
        "playlist_title": video_metadata["playlist_title"],
        "published_time_text": published_time_text,
        "retrieved_time": str(datetime.datetime.utcnow()),
    }

    processed_local_path = f"data/{video_id}.json"
    with open(processed_local_path, "w") as _file:
        json.dump(video, _file, indent=4)

    os.remove(_video_metadata_file)
    print(f"Wrote {processed_local_path}")
