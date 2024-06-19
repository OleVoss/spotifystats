import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
import spotipy
import numpy as np
from spotipy.oauth2 import SpotifyClientCredentials
import time

request_timer = 0.33
person = "hennes"
data_path = "./data/" + person

paths = Path(data_path).glob("Streaming*.json")
df = pd.concat(map(pd.read_json, paths))
df = df[df["spotify_track_uri"].notnull()]

### track table
unique_tracks = df[df["episode_name"].isnull()][
    [
        "master_metadata_track_name",
        "master_metadata_album_album_name",
        "spotify_track_uri",
        "master_metadata_album_artist_name",
    ]
].drop_duplicates()
unique_tracks = unique_tracks.dropna()
unique_tracks.to_csv("./processed/" + person + "/unique_tracks.csv")
