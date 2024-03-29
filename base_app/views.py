from django.shortcuts import render
from base_app.models import Workers
from django.http import HttpResponse
from tubefox import TubeFox


def index_page(request):
    if request.method == "POST":
        data = request.POST
        yt_object = TubeFox(data['yt_link'])
        return render(request, 'index.html',
                      {'title': yt_object.title,
                       'description': yt_object.description,
                       'keywords': yt_object.keywords,
                       'download_video': yt_object.app_collected_data.collect_video_links()
                       [max(yt_object.app_collected_data.collect_video_links().keys())],
                       'download_thumbnail': yt_object.web_collected_data.collect_thumbnail_links()
                       [max(yt_object.web_collected_data.collect_thumbnail_links().keys())],
                       'download_audio': yt_object.app_collected_data.collect_audio_links()
                       [max(yt_object.app_collected_data.collect_audio_links().keys())],
                       }
                      )
    elif request.method == "GET":
        return render(request, 'index.html')

