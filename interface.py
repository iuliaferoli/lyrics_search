from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import json

app = FastAPI()

class Song(BaseModel):
    name: str
    artist: str
    lyrics: str | None
    id : int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Take me to church",
                    "artist": "Hozier",
                    "lyrics": "Her eyes and words are so icy\nOh but she burns\nLike rum on the fire",
                    "id": 0,
                }
            ]
        }
    }



@app.get("/songs/{id}")
def read_root(id:int):
    # get song based on Id
    # display song
    # for testing - we just use the json file for now
    with open('hozier_songs.json', 'r') as f:
        songs = json.load(f)
    song = Song.model_validate(songs[id])
    return song


@app.get("/search/{query}")
def search_item(query: str):
    # get list of songs based on query
    # display songs & lyrics
    return {}


@app.put("/songs/{song_id}")
def save_item(song_id: int, song: Song):
    #add song to index
    return {"Song added to the index"}