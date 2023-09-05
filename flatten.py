import json
from os import listdir
from os.path import isfile, join
from pprint import pprint

videos = [
    f
    for f in listdir("data/transcriptions_raw")
    if isfile(join("data/transcriptions_raw", f))
]

for video in videos:
    with open(f"data/transcriptions_raw/{video}") as _file:
        transcription = json.load(_file)
        merged = ""
        for part in transcription:
            merged += f" {part['text']} "
        merged = merged.replace("  ", " ")
    video_id = video.replace(".json", "")
    with open(f"data/transcriptions_flattened/{video_id}.txt", "w") as _file:
        _file.write(merged)
