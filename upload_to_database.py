import pandas as pd
import os
from pathlib import Path
from sqlalchemy import create_engine

import csv
from io import StringIO

def psql_insert_copy(table, conn, keys, data_iter): #mehod
    """
    Execute SQL statement inserting data

    Parameters
    ----------
    table : pandas.io.sql.SQLTable
    conn : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
    keys : list of str
        Column names
    data_iter : Iterable that iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)

def tryconvert(value, default, *types):
    for t in types:
        try:
            return t(value)
        except (ValueError, TypeError):
            continue
    return default

def tracks(person):
    try:
        tracks = pd.read_csv("./spotify_downloads/" + person + "/tracks_with_features.csv").rename({"mode":"is_major","master_metadata_track_name": "track_name", "spotify_track_uri":"track_uri", "master_metadata_album_album_name": "album_name", "duration_ms_x": "duration_ms"}, axis=1).drop(["Unnamed: 0", "duration_ms_y"], axis=1)
        tracks = tracks.drop_duplicates(subset=["isrc"])
        tracks["is_major"] = tracks["is_major"].map(lambda r:bool(r))
        tracks["explicit"] = tracks["explicit"].map(lambda r:bool(r))
        tracks["key"] = tracks["key"].map(lambda r:tryconvert(r, -1, int))
        tracks["time_signature"] = tracks["time_signature"].map(lambda r:tryconvert(r, -1, int))
        tracks.to_sql("track", engine, if_exists="append", method=psql_insert_copy, index=False)
    except Exception as e:
        print(e)
        engine.dispose()
    finally:
        engine.dispose()

def artist_track(person):
    try:
        artist_track = pd.read_csv("./spotify_downloads/" + person + "/artist_track.csv")
        artist_track.to_sql("artist_track", engine, if_exists="append", method=psql_insert_copy, index=False)
    except Exception as e:
        print(e)
        engine.dispose()
    finally:
        engine.dispose()

def play(person):
    try:
        artist_track = pd.read_csv("./spotify_downloads/" + person + "/artist_track.csv")
        artist_track.to_sql("artist_track", engine, if_exists="append", method=psql_insert_copy, index=False)
    except Exception as e:
        print(e)
        engine.dispose()
    finally:
        engine.dispose()
        


person = "selina"
engine = create_engine("postgresql://postgres:whhBQCALKS132zN@localhost:5432/postgres")

# artist_track(person)