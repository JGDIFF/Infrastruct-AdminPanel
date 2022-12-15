import firebase_admin
import pandas as pd
import plotly.express as px
from firebase_admin import credentials
from firebase_admin import firestore
import json
import os

#Using a service account.
cred = credentials.Certificate('connection.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()
users_ref = db.collection(u'Reports')
docs = users_ref.stream()

dictObj = { el.id: el.to_dict() for el in docs }

with open("sample.json", "w") as outfile:
    json.dump(dictObj, outfile)

with open('sample.json', encoding='utf-8') as inputfile:
    data = json.load(inputfile)
    df = pd.json_normalize(data[k] for k in data.keys())

df.to_csv("outputfile.csv", index=False)

df = pd.read_csv("outputfile.csv")

color_scale = [(0, 'orange'), (1,'red')]
fig = px.scatter_mapbox(df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="reportType",
                        hover_data=["user"],
                        color="reportType",
#                        color_continuous_scale=color_scale,
#                        size=3,
                        zoom=2,
                        height=800,
                        width=800)


#fig = px.scatter_mapbox(df,
#                        lat="Lat",
#                        lon="Long",
#                        hover_name="Address",
#                        hover_data=["Address", "Listed"],
#                        color="Listed",
#                        color_continuous_scale=color_scale,
#                        size="Listed",
#                        zoom=8,
#                        height=800,
#                        width=800)



fig.update_layout(mapbox_style="open-street-map")
fig.show()