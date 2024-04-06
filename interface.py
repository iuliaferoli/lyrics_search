from fastapi import FastAPI
import json

with open('hozier_songs.json', 'r') as f:
  songs = json.load(f)

app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome to the demo"


@app.get("/songs/{song_id}")
def read_item(song_id: int):
    # get song with this id
    # display song & lyrics
    return {}


@app.get("/search/{query}")
def search_item(query: str):
    # get list of songs based on query
    # display songs & lyrics
    return {songs[0]["artist"]: songs[0]["name"]}


@app.put("/songs/{song_id}")
def save_item(song_id: int, song: dict):
    return {"Song added to the index"}