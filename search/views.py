from django.shortcuts import render
from django.conf import settings
import requests
from isodate import parse_duration
from operator import itemgetter


def index(request):
    videos = []
    if request.method == "POST":
        search_url = "https://www.googleapis.com/youtube/v3/search"
        video_url = "https://www.googleapis.com/youtube/v3/videos"

        params = {
            "part": "snippet",
            "q": request.POST["search"],
            "key": settings.YOUTUBE_DATA_API_KEY,
            "maxResults": 9,
            "type": "video"
        }

        video_ids = []

        r = requests.get(search_url, params=params)
        results = r.json()["items"]

        for result in results:
            video_ids.append(result["id"]["videoId"])

        video_params = {
            "key": settings.YOUTUBE_DATA_API_KEY,
            "part": "snippet,contentDetails",
            "id": ','.join(video_ids)
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()["items"]

        for result in results:
            # print(parse_duration(
            #     result["contentDetails"]["duration"]).total_seconds())
            video_data = {
                "title": result["snippet"]["title"],
                "published": result["snippet"]["publishedAt"],
                "id": result["id"],
                "duration": int(parse_duration(result["contentDetails"]["duration"]).total_seconds()//60),
                "thumbnail": result["snippet"]["thumbnails"]["high"]["url"],
                "url": f'https://www.youtube.com/watch?v={result["id"]}'
            }
            videos.append(video_data)

        videos = sorted(videos, key=itemgetter("published"), reverse=True)
        print(videos)
    context = {
        "videos": videos
    }

    return render(request, "search/index.html", context)
