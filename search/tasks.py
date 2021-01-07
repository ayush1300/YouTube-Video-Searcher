from django.shortcuts import render
from django.conf import settings
import requests
from isodate import parse_duration
from operator import itemgetter
from django.core.paginator import Paginator
from .models import Videos
from background_task import background

# background running tasks


@background(schedule=60)
def demo_task():
    videos = []

    # these are urls as mentioned in youtube api docs using which the requests are made
    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_url = "https://www.googleapis.com/youtube/v3/videos"

    # parameters which needs to be passed for getting the video ids according to search query
    # q refers to the search query
    params = {
        "part": "snippet",
        "q": "cricket",
        "key": settings.YOUTUBE_DATA_API_KEY,
        "maxResults": 60,
        "type": "video"
    }

    video_ids = []

    # GET request to get the data
    r = requests.get(search_url, params=params)
    # print(r.json())
    results = r.json()['items']

    # storing the video Ids
    for result in results:
        video_ids.append(result["id"]["videoId"])

    # adding the video parameters so that we can get appropriate data of the video Ids previously fetched
    video_params = {
        "key": settings.YOUTUBE_DATA_API_KEY,
        "part": "snippet,contentDetails",
        "id": ','.join(video_ids),
    }
    # Making the GET request to get the data of the video ids
    r = requests.get(video_url, params=video_params)

    results = r.json()['items']
    # print(r.json())

    # for fetching the data that we require we add all the required information in a list of dictionary
    for result in results:
        video_data = {
            "title": result["snippet"]["title"],
            "published": result["snippet"]["publishedAt"],
            "id": result["id"],
            "duration": int(parse_duration(result["contentDetails"]["duration"]).total_seconds()//60),
            "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
            "url": f'https://www.youtube.com/watch?v={result["id"]}'
        }
        videos.append(video_data)

    # sorting the videos in reverse chronological order
    # videos = sorted(videos, key=itemgetter("published"), reverse=True)
    for video in videos:
        v = Videos()
        v.title = video["title"]
        v.published = video["published"]
        v.videoId = video["id"]
        v.tag = "cricket"
        v.duration = video["duration"]
        v.thumbnail = video["thumbnail"]
        v.url = video["url"]

        v1 = Videos.objects.filter(videoId=v.videoId)
        # print(v1)
        if v1.count() == 0:
            v.save()
