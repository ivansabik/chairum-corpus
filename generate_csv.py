import json
from os import listdir
from os.path import isfile, join

import pandas as pd

videos = [f for f in listdir("data") if isfile(join("data", f))]

all_data = []
for video in videos:
    with open(f"data/{video}") as _file:
        data = json.load(_file)
        all_data.append(data)
df = pd.DataFrame(all_data)
df.to_csv("data.csv", index=False)
