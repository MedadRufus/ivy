from pathlib import Path
import json
import plotly.express as px
import pandas as pd
from json.decoder import JSONDecodeError
import logging

target_env = "jackson_hole.env"

logs_dir = Path("../data/logs")

files = logs_dir.glob('*.log')


data = []

for i in files:
    data_in_this_file = i.read_text().splitlines()
    for i in data_in_this_file:
        try:

            i = json.loads(i)
            if i["meta"]["argfile"] == target_env:
                print(i)
                data+=data_in_this_file
                break
        except KeyError:
            pass
            #print("key error")
        except JSONDecodeError:
            print("json decode error")

timestamps = []

for i in data:
    try:
        if i["level"] == "INFO" and i["meta"]["label"] == "OBJECT_COUNT":
            timestamps.append(i["meta"]["counted_at"])
    except TypeError:
        pass




df = pd.Series(timestamps)
df = pd.to_datetime(df, unit='s')
fig = px.histogram(df, nbins=80)
fig.show()


#{"created": 1609751979.5856664, "logger": "job_1609751970_d835573a325b4aee9a394a187f11bb57", "level": "INFO", "message": "Processing started.", "meta": {"label": "START_PROCESS", "counter_config": {"di": 10, "mcdf": 2, "mctf": 3, "detector": "yolo", "tracker": "kcf", "use_droi": true, "droi": [[0, 367], [1913, 243], [1913, 1076], [0, 1078]], "counting_lines": [{"label": "A", "line": [[425, 698], [915, 812]]}, {"label": "B", "line": [[1112, 716], [1781, 783]]}], "argfile": "jackson_hole.env"}}}