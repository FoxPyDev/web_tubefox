from django.shortcuts import render
from tubefox import TubeFox


def index_page(request):
    if request.method == "POST":
        data = request.POST
        try:
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
        except:
            return render(request, 'index.html')
    elif request.method == "GET":
        return render(request, 'index.html')


def bootstrap_page(request):
    return render(request, 'bootstrap.html')

