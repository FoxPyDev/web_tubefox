from django.shortcuts import render, HttpResponse
import requests
from tubefox import TubeFox
from tubefox.yt_app_version_updater import get_yt_app_latest_version
from tubefox.subtitles import Subtitles


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


# def bootstrap_page(request):
#     return render(request, 'bootstrap.html')


def bootstrap_page(request):
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            return render(request, 'bootstrap.html',
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
            return render(request, 'bootstrap.html')
    elif request.method == "GET":
        return render(request, 'bootstrap.html')


def download_video(request):
    if request.method == "POST":
        video_url = request.POST.get('download_video')
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'com.google.android.youtube/{get_yt_app_latest_version()} (Linux; U; Android 12; GB) gzip'
        }
        video_response = requests.get(video_url, stream=True, headers=headers)

        if video_response.status_code == 200 and 'Content-Length' in video_response.headers:
            content_length = int(video_response.headers['Content-Length'])
            if content_length > 0:
                response = HttpResponse(video_response.content, content_type='video/mp4')
                response['Content-Disposition'] = 'attachment; filename="video.mp4"'
                return response

        return HttpResponse("Reload page and try again")

def metadata_page(request):
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            return render(request, 'metadata.html',
                          {'title': yt_object.title,
                           'description': yt_object.description,
                           'keywords': yt_object.keywords,
                           'status': 'ok'
                           }
                          )
        except:
            return render(request, 'metadata.html',
                          {'status': 'no info'})
    elif request.method == "GET":
        return render(request, 'metadata.html')

def thumbnail_page(request):
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            return render(request, 'thumbnail.html',
                          {'title': yt_object.title,
                           'download_thumbnail': yt_object.web_collected_data.collect_thumbnail_links()
                           [max(yt_object.web_collected_data.collect_thumbnail_links().keys())]}
                          )
        except:
            return render(request, 'thumbnail.html')
    elif request.method == "GET":
        return render(request, 'thumbnail.html')


def subtitles_page(request):
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            all_subtitles = yt_object.web_collected_data.collect_subtitles_links()

            # Перетворюємо словник у список пар (ключ, значення)
            subtitles_list = list(all_subtitles.items())

            return render(request, 'subtitles.html', {'title': yt_object.title,
                                                      'subtitles_list': subtitles_list})
        except:
            return render(request, 'subtitles.html')
    elif request.method == "GET":
        return render(request, 'subtitles.html')


def save_to_txt(request):
    if request.method == "POST":
        link = request.POST.get('subtitles_link')
        txt_content = Subtitles(link).subtitles_to_text
        response = HttpResponse(txt_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="subtitle.txt"'
        return response


def save_to_srt(request):
    if request.method == "POST":
        link = request.POST.get('subtitles_link')
        txt_content = Subtitles(link).subtitles_to_srt
        response = HttpResponse(txt_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="subtitle.srt"'
        return response
