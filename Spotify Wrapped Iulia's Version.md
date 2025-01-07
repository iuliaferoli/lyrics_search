# Spotify Wrapped Iulia's Version.

I am probably not the only one who was a little dissapointed by the Spotify Wrapped this year (and the internet seems to agree). Looking back at our yearly musical history has become a highly anticipated moment of the year for heavy Spotify users. However, at the end of the day all "Wrapped" is, is a data analytics problem, with a great PR team. So perhaps the mantle must fall on fellow data analysts to attempt to solve this problem in a more satisfying way. 

With the back-to-work and brand-new-year motivation fueling us - let's see if we can do any better. (spoiler alert: definitely!)

### Getting your listening data 

The best part about this exercise is that it's fully replicable. Spotify allows users [to download their own historical streaming data via this link.](https://www.spotify.com/uk/account/privacy/), which you can request out of your account settings.

Once this has been generated we can dive into years worth of data and start building our own fun dashboards. Check out [this notebook](/define_music_list.ipynb) for the code eamples.

Historical data will be generated as a list of JSON documents, each of them representing an action - in most cases a song that you've listened to with some additional metadata such as length of time in miliseconds, artist information, as well as device properties. Naturally, if you have any experience with Elastic, the first thought looking at this data would be that this data practically screams "add me to an index and search me!". So we will do just that.

### Building an Elasticsearch Index

As you can see in [the same notebook]() once we've connected to our preferred Elasticsearch client, it takes a few simple lines of code to send the json documents into a new index:

```python
def generate_docs(DATASET_PATH):
    with open(DATASET_PATH, "r") as f:
        json_data = json.load(f)
        documents = []
        for doc in json_data:
            documents.append(doc)
        load = helpers.bulk(client, documents, index=index_name)
```

Even the mapping is handleled automatically due to the high quality and consistency of the data as prepared by Spotify. One key element to pay attention to is to ensure fields like "Artist Name" are seen as `keywords` which will allow us to run more complex aggregations for our dashboards.

### Wrapping Queries

With the index fully populated we can explore the data throuhg code to run a few simple test queries. My top artist has been Hozier for quite a few years now, so I start with the simplest possible term query to check my data:

```python

index_name = 'spotify-history'
query={
    "match": {
        "master_metadata_album_artist_name": "Hozier"
    }
}

response = client.search(index=index_name, query=query, size=3)

print("We get back {total} results, here are the first ones:".format(total=response["hits"]['total']['value']))
for hit in response["hits"]["hits"]:
    print(hit['_source']["master_metadata_track_name"])
```

This gives me back 5653 hits - which means I've played more than 5 thousand Hozier songs since 2015 (as far as my data goes back). Seems pretty accurate. 

Now we can continue to build more complex queries via code (or equivalent queries we can test with tools like the Dev Console). 

Like the most anticipated question - is my top artist list in Wrapped accurate? 
You can see in this notebook how we can build aggregations in our query to see the top artists. 

We can run this by either number of hits (how many songs have been played) or perhaps more accurately, by summing up the total number of milliseconds of playtime by artist bucket.
![](img/code%20query.png)

[See some great content on aggregation](https://opster.com/guides/elasticsearch/search-apis/elasticsearch-filter-aggregation/) @elisheva - should this be an elasticsearch link instead? opster had some awesome content on this.

### Building Dashboards

After these few examples we should have a good understanding of the Elasticsearc mechanics we can use to drill into this data. However, to both save time and make the insights more consumable (and pretty) we can also build a lot of these insights directly in a Kibana dashboard. 
Moving to my cloud Elastic cluster I've built a data view from my index and I can now directly build visualizations by dragging my data fields and choosing view types.

Within a few hours we have Iulia's Version of Spotify Wrapped, going deeper than ever before. Let's take a look.

![](img/rank.png)

Starting with the "classic" wrapped insights - we can easily build the top artist and song rank.

Here's an example of how one of these graphs is built:

![](img/top.png)

Looking at the points of interest in this graph:
* make sure to selecr the correct time interval for our data to cover 2024 in `1`
* choose to show the `top values` of the artist name field, and exclude the `other` bucket to make our visualization neat in `2`
* map this against the count of records to rank the artists based on how many times they appear in the data (equivalent to time the songs were played) in `3`


However, we can go further by adding more metadata like time or location and looking at how these trends have changed throughout the year. Here we can see the listening time over the year (in weekly buckets), the locations I've been listening from while traveling, and how my top artists have varied month by month (including a sighting of brat girl summer).

![](img/advanced.png)


![](/img/time.png)

Some more tricks worth noting for these graphs:
* When we work with the playing time instead of just count of records, we choose to aggregate all the instances of a song or artist being played by using the `sum` function. This is kibana equivalend to the `aggs` opertor we were using in the code in the first [notebook](/define_music_list.ipynb) examples.
* You can additionaly convert the milisecond into minutes or hours for neater visualiation
* Finally we add the `top 3 artists name` as an additional breakdown in this graph


Comparing this to my acutal Wrapped - it seems the results were close enough, but maybe not entierly accurate. It seems this year the top song choices are a little off from the way I calculate my ranking in this example. It could be that Spotify used a different formula to build this ranking, which makes it a bit harder to interpret. Thats's one of the benefits of building this dashboard from scratch - you have full transparancy on the type of aggregations and scoring used for your insights.

![](img/wrapped.jpeg)

And this is only scratching the surface of possible visualizations; I can already imagine for certain artists it would be interesting to look at different angles like Top album (or era). 

![](img/album.png)

Just having the data stored in an index makes this a really fun and simple Elasticsearch use case, really showcasing some of the coolest features like aggregations or custom dashboarding.

This already feels more interesting to look at than the simple ranking we got this year, so I will definitely re-run this script and dashboard with my Spotify data from now on - and feel free to try it out for yourself! 
