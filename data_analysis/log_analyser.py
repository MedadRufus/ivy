from pathlib import Path
import json
import plotly.express as px
import pandas as pd


target_env = "casa_grande.env"

logs_dir = Path("../data/logs")

files = logs_dir.glob('*.log')


data = []

for i in files:
    data += i.read_text().splitlines()

timestamps = []

for i in data:
    i = json.loads(i)

    if i["meta"]["label"] == "START_PROCESS":
        print(i)

    if i["level"] == "INFO":
        if i["meta"]["label"] == "OBJECT_COUNT":
            timestamps.append(i["meta"]["counted_at"])

df = pd.Series(timestamps)
df = pd.to_datetime(df, unit='s')
fig = px.histogram(df, nbins=80)
fig.show()


#{"created": 1609700680.2017016, "logger": "job_1609700677_087ed602b4ed4299a12d20729063e451", "level": "INFO", "message": "Processing started.", "meta": {"label": "START_PROCESS", "counter_config": {"di": 10, "mcdf": 2, "mctf": 3, "detector": "yolo", "tracker": "csrt", "use_droi": true, "droi": [[0, 345], [980, 210], [1229, 266], [513, 712]], "counting_lines": [{"label": "A", "line": [[158, 321], [266, 374]]}, {"label": "B", "line": [[931, 450], [664, 368]]}]}}}