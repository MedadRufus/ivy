
def get_data_html():
    import pandas as pd
    import pickle

    df = pickle.load(open("./data_analysis/tokyo_crosswalk_weather_df.p", "rb"))



    def convert_to_numeric(df, col):
        df[col] = df[col].str.extract(r'(\d+)')
        df[col] = pd.to_numeric(df[col])



    def prep_for_mongo(df):
        convert_to_numeric(df, "Wind Speed")
        convert_to_numeric(df, "Dew Point")
        convert_to_numeric(df, "Humidity")
        convert_to_numeric(df, "Wind Gust")
        convert_to_numeric(df, "Pressure")
        convert_to_numeric(df, "Precip.")
        convert_to_numeric(df, "Temperature")

        df = df.rename(columns={"Precip.": "Precipitation"})
        return df


    # In[15]:


    df = prep_for_mongo(df)





    pipeline = [
        {
            '$addFields': {
                'datetime': {
                    '$toDate': {
                        '$multiply': [
                            '$counted_at', 1000
                        ]
                    }
                }
            }
        }, {
            '$addFields': {
                'counted_at': {
                    '$convert': {
                        'input': '$counted_at',
                        'to': 'double',
                        'onError': None
                    }
                },
                'computer_id': {
                    '$convert': {
                        'input': '$computer_id',
                        'to': 'string',
                        'onError': None
                    }
                }
            }
        }, {
            '$match': {
                'arg_file': {
                    '$in': [
                        'jackson_hole.env'
                    ]
                },
                'type': {
                    '$nin': []
                },
                'computer_id': {
                    '$in': [
                        None, '', '00000000-0000-0000-0000-3cecef225486', '00000000-0000-0000-0000-f894c218ae25'
                    ]
                },
            }
        }, {
            '$addFields': {
                'datetime': {
                    '$cond': {
                        'if': {
                            '$eq': [
                                {
                                    '$type': '$datetime'
                                }, 'date'
                            ]
                        },
                        'then': '$datetime',
                        'else': None
                    }
                }
            }
        }, {
            '$addFields': {
                '__alias_0': {
                    'year': {
                        '$year': '$datetime'
                    },
                    'month': {
                        '$subtract': [
                            {
                                '$month': '$datetime'
                            }, 1
                        ]
                    },
                    'date': {
                        '$dayOfMonth': '$datetime'
                    },
                    'hours': {
                        '$hour': '$datetime'
                    },
                    'minutes': {
                        '$minute': '$datetime'
                    }
                }
            }
        }, {
            '$group': {
                '_id': {
                    '__alias_0': '$__alias_0'
                },
                '__alias_1': {
                    '$sum': {
                        '$cond': [
                            {
                                '$ne': [
                                    {
                                        '$type': '$datetime'
                                    }, 'missing'
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0,
                '__alias_0': '$_id.__alias_0',
                '__alias_1': 1
            }
        }, {
            '$project': {
                'x': '$__alias_0',
                'y': '$__alias_1',
                '_id': 0
            }
        }, {
            '$sort': {
                'x.year': 1,
                'x.month': 1,
                'x.date': 1,
                'x.hours': 1,
                'x.minutes': 1
            }
        }
    ]

    # In[74]:


    # init mongo connection
    from pymongo import MongoClient
    import urllib.parse
    import datetime
    import pandas as pd

    username = urllib.parse.quote_plus('dbUser')
    password = urllib.parse.quote_plus("PwBhv72bEOq4NGlI")
    url = "mongodb+srv://{}:{}@cluster0.edygp.mongodb.net/test?retryWrites=true&w=majority".format(username, password)
    client = MongoClient(url)


    def get_data(pipeline):
        traffic_results = client["traffic"]["traffic_data"].aggregate(pipeline)

        traffic_results = list(traffic_results)
        traffic_results.pop(0)

        for i in traffic_results:
            try:
                i["x"] = datetime.datetime(year=i["x"]["year"], month=i["x"]["month"] + 1, day=i["x"]["date"],
                                           hour=i["x"]["hours"])
            except TypeError:
                pass

        traffic_df = pd.DataFrame.from_records(traffic_results)
        return traffic_df


    def gen_pipeline(env_file):
        a = pipeline.copy()
        a[2]["$match"]["arg_file"]["$in"][0] = env_file
        return a


    def remove_duplicates(df):
        return df.groupby(['x'], as_index=False)['y'].sum()


    # In[79]:


    jackson_traffic_df = get_data(gen_pipeline("jackson_hole.env"))
    jackson_traffic_df = remove_duplicates(jackson_traffic_df)

    casa_grande_traffic_df = get_data(gen_pipeline("casa_grande.env"))
    casa_grande_traffic_df = remove_duplicates(casa_grande_traffic_df)

    tokyo_crosswalk_traffic_df = get_data(gen_pipeline("tokyo_crosswalk.env"))
    tokyo_crosswalk_traffic_df = remove_duplicates(tokyo_crosswalk_traffic_df)




    # from plotly.subplots import make_subplots
    # import plotly.graph_objects as go
    # import plotly.io as pio
    #
    # pio.renderers.default = 'browser'
    #
    # fig = make_subplots(rows=3, cols=1)
    #
    # fig.append_trace(go.Bar(
    #
    #     x=jackson_traffic_df["x"],
    #     y=jackson_traffic_df["y"],
    #     name="Jackson Hole traffic"
    #
    # ), row=1, col=1)
    #
    # fig.append_trace(go.Bar(
    #     x=casa_grande_traffic_df["x"],
    #     y=casa_grande_traffic_df["y"],
    #     name="Casa Grande Traffic"
    # ), row=2, col=1)
    #
    # fig.append_trace(go.Bar(
    #     x=tokyo_crosswalk_traffic_df["x"],
    #     y=tokyo_crosswalk_traffic_df["y"],
    #     name="Tokyo Cross Walk"
    #
    # ), row=3, col=1)
    #
    # fig.update_layout(title_text="Human and Vehicle traffic data")
    #fig.show()

    # # Now get back the weather data from the db

    # In[218]:

    #
    # pipeline_weather = [
    #     {
    #         "$group": {
    #             "_id": {
    #                 "__alias_0": "$Time",
    #                 "__alias_1": "$Dew Point",
    #                 "__alias_2": "$Wind Gust",
    #                 "__alias_3": "$Wind Speed",
    #                 "__alias_4": "$Temperature",
    #                 "__alias_5": "$Pressure"
    #             }
    #         }
    #     },
    #     {
    #         "$project": {
    #             "_id": 0,
    #             "__alias_0": "$_id.__alias_0",
    #             "__alias_1": "$_id.__alias_1",
    #             "__alias_2": "$_id.__alias_2",
    #             "__alias_3": "$_id.__alias_3",
    #             "__alias_4": "$_id.__alias_4",
    #             "__alias_5": "$_id.__alias_5"
    #         }
    #     },
    #     {
    #         "$project": {
    #             "x": "$__alias_0",
    #             "y": "$__alias_1",
    #             "y_series_0": "$__alias_2",
    #             "y_series_1": "$__alias_3",
    #             "y_series_2": "$__alias_4",
    #             "y_series_3": "$__alias_5",
    #             "_id": 0
    #         }
    #     },
    #     {
    #         "$sort": {
    #             "x": 1,
    #             "y": 1,
    #             "y_series_0": 1,
    #             "y_series_1": 1,
    #             "y_series_2": 1,
    #             "y_series_3": 1
    #         }
    #     },
    #     {
    #         "$addFields": {
    #             "__multi_series": {
    #                 "$objectToArray": {
    #                     "Wind Gust": "$y_series_0",
    #                     "Wind Speed": "$y_series_1",
    #                     "Temperature": "$y_series_2",
    #                     "Pressure": "$y_series_3",
    #                     "Dew Point": "$y"
    #                 }
    #             }
    #         }
    #     },
    #     {
    #         "$unwind": "$__multi_series"
    #     },
    #     {
    #         "$addFields": {
    #             "color": "$__multi_series.k",
    #             "y": "$__multi_series.v"
    #         }
    #     },
    #     {
    #         "$project": {
    #             "__multi_series": 0,
    #             "y_series_0": 0,
    #             "y_series_1": 0,
    #             "y_series_2": 0,
    #             "y_series_3": 0
    #         }
    #     },
    #     {
    #         "$limit": 50000
    #     }
    # ]
    #
    # # In[219]:
    #
    #
    # weather_results = client["weather"]["jackson_hole"].aggregate(pipeline_weather)
    # list(weather_results)

    # In[19]:

    #
    # import plotly.express as px
    # import plotly.io as pio
    #
    # pio.renderers.default = 'browser'
    #
    # fig = px.line(df, x="Time",
    #               y=df[["Temperature", "Dew Point", "Wind Speed", "Wind Gust", "Pressure", "Precipitation"]].columns)
    # fig
    # #fig.show()

    # In[55]:


    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import plotly.io as pio

    pio.renderers.default = 'browser'

    values = ["Temperature", "Wind Speed", "Wind Gust"]
    fig = make_subplots(rows=len(values) + 2, cols=1, shared_xaxes=True,)

    fig.append_trace(go.Bar(

        x=tokyo_crosswalk_traffic_df["x"],
        y=tokyo_crosswalk_traffic_df["y"],
        name="Tokyo traffic"

    ), row=1, col=1)

    for i in range(len(values)):
        fig.append_trace(go.Scatter(

            x=df["Time"],
            y=df[values[i]],
            mode='lines',

            name=values[i]
        ), row=i + 2, col=1)

    fig.append_trace(go.Scatter(

        x=df["Time"],
        y=df["Condition"],
        name="Condition",
        mode="markers",

    ), row=len(values) + 2, col=1)



    fig.update_layout(title_text="Human and Vehicle traffic data combined with weather data for Tokyo Crosswalk")
    # Use date string to set xaxis range
    fig.update_layout(xaxis_range=['2021-01-05', '2021-1-13'])


    return fig.to_html(full_html=False)




    # /html/body/app-root/app-today/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[3]/div[1]/div/div[1]/div[1]/lib-city-current-conditions/div
