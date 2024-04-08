# Using Elasticsearch to build the ultimate song finder


Using [an API service](/get_lyrics_musixmatch.ipynb) we can gather and pre-process song lyrics for our dataset.
[X] Get lyrics sample
[ ] Get larger lyrics dataset based on streaming history

We can then [connect to Elasticsearch](/elasticsearch.ipynb) and index this data, allowing us to search through lyrics - at first with basic matches, then with the ELSER semantic model which allows us to look through the lyrics' meaning. 
[X] Build index
[X] Semantic search POC
[ ] Expand with Spotify data

To expand our project, we can download personal listening histories from a streaming service and combine this with our lyrics data. This was we can create hybrid, personalized searches depending on preference, mood, and meaning. 
[ ] Get and process Spotify data
[ ] Make Kibana Dashboard, similar to Spotify Wrapped

Finally, we [can build a simple web interface](/interface.py) to allow us to run the searches on the go.
[X] Build fastAPI POC
[ ] Connect interface to ES backend