#!/usr/bin/env python
# coding: utf-8

# In[90]:


from pathlib import Path
import json
import plotly.express as px
import pandas as pd
from json.decoder import JSONDecodeError
import logging


# In[91]:


#target_env = "casa_grande.env"
target_env = "jackson_hole.env"
#target_env = "tokyo_crosswalk.env"

logs_dir = Path("../data/logs")

files = list(logs_dir.glob('*.log'))


# In[92]:


data = []

for f in files:
    data_in_this_file = f.read_text().splitlines()
    for line in data_in_this_file:
        try:
            if target_env in line:
                data += data_in_this_file
                break
        except KeyError:
            print("key error")
        except JSONDecodeError:
            print("json decode error")


# In[93]:


len(data)


# In[94]:


timestamps = []

for i in data:
    i = json.loads(i)
    try:
        if i["meta"]["label"] == "OBJECT_COUNT":
            timestamps.append(i["meta"]["counted_at"])
    except KeyError:
        pass


# In[1]:


import plotly.io as pio
pio.renderers.default = 'browser'

df = pd.Series(timestamps)
df = pd.to_datetime(df, unit='s')
fig = px.histogram(df)


fig.update_traces(xbins=dict( # bins used for histogram
        size=900000/3 # 15 minutes in milliseconds
    ))
fig.write_html("output.html")
fig.show()


# In[ ]:





# In[ ]:




