import json
import os

import pandas as pd

videos = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]

all_data = []
for video in videos:
    with open(f"data/{video}") as _file:
        data = json.load(_file)
        all_data.append(data)
df = pd.DataFrame(all_data)
df.to_csv("data.csv", index=False)
