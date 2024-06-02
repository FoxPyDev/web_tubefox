from django.shortcuts import render, HttpResponse
import requests
from tubefox import TubeFox
from tubefox.yt_app_version_updater import get_yt_app_latest_version
from tubefox.subtitles import Subtitles
from django.http import StreamingHttpResponse
import moviepy.editor as mp
from io import BytesIO
import tempfile


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
                           'download_muted_video': yt_object.app_collected_data.collect_muted_video_links()
                           [max(yt_object.app_collected_data.collect_muted_video_links().keys())],
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
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            return render(request, 'bootstrap.html',
                          {'title': yt_object.title,
                           'download_video': yt_object.app_collected_data.collect_video_links()
                           [max(yt_object.app_collected_data.collect_video_links().keys())],
                           'download_muted_video': yt_object.app_collected_data.collect_muted_video_links()
                           [max(yt_object.app_collected_data.collect_muted_video_links().keys())],
                           'download_thumbnail': yt_object.web_collected_data.collect_thumbnail_links()
                           [max(yt_object.web_collected_data.collect_thumbnail_links().keys())],
                           'status': 'ok'
                           }
                          )
        except:
            return render(request, 'bootstrap.html',
                          {'status': 'no info'})
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
                response = StreamingHttpResponse(
                    (chunk for chunk in video_response.iter_content(chunk_size=8192)),
                    content_type='video/mp4'
                )
                response['Content-Disposition'] = 'attachment; filename="video.mp4"'
                return response

        return HttpResponse("Reload page and try again")


def download_muted_video(request):
    if request.method == "POST":
        video_url = request.POST.get('download_muted_video')
        print(video_url)
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'com.google.android.youtube/{get_yt_app_latest_version()} (Linux; U; Android 12; GB) gzip'
        }
        video_response = requests.get(video_url, stream=True, headers=headers)

        if video_response.status_code == 200 and 'Content-Length' in video_response.headers:
            content_length = int(video_response.headers['Content-Length'])
            if content_length > 0:
                response = StreamingHttpResponse(
                    (chunk for chunk in video_response.iter_content(chunk_size=8192)),
                    content_type='video/mp4'
                )
                response['Content-Disposition'] = 'attachment; filename="muted_video.mp4"'
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
                           [max(yt_object.web_collected_data.collect_thumbnail_links().keys())],
                           'status': 'ok'}
                          )
        except:
            return render(request, 'thumbnail.html',
                          {'status': 'no info'})
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
                                                      'subtitles_list': subtitles_list,
                                                        'status': 'ok'})
        except:
            return render(request, 'subtitles.html',
                          {'status': 'no info'})
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


def download_thumbnail(request):
    if request.method == "POST":
        thumbnail_url = request.POST.get('thumbnail_link')

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'com.google.android.youtube/{get_yt_app_latest_version()} (Linux; U; Android 12; GB) gzip'
        }

        try:
            image_response = requests.get(thumbnail_url, stream=True, headers=headers)
        except requests.RequestException as e:
            return render(f"Error fetching the image: {e}")

        if image_response.status_code == 200 and 'Content-Length' in image_response.headers:
            content_length = int(image_response.headers['Content-Length'])
            if content_length > 0:
                content_type = image_response.headers.get('Content-Type', 'image/jpeg')
                file_extension = content_type.split('/')[-1] if '/' in content_type else 'jpg'
                response = HttpResponse(image_response.content, content_type=content_type)
                response['Content-Disposition'] = f'attachment; filename="thumbnail.{file_extension}"'
                return response


def audio_page(request):
    if request.method == "POST":
        data = request.POST
        try:
            yt_object = TubeFox(data['yt_link'])
            return render(request, 'audio.html',
                          {'title': yt_object.title,
                           'download_thumbnail': yt_object.web_collected_data.collect_thumbnail_links()
                           [max(yt_object.web_collected_data.collect_thumbnail_links().keys())],
                           'download_video': yt_object.app_collected_data.collect_video_links()
                           [max(yt_object.app_collected_data.collect_video_links().keys())],
                           'status': 'ok'}
                          )
        except:
            return render(request, 'audio.html',
                          {'status': 'no info'})
    elif request.method == "GET":
        return render(request, 'audio.html')


def download_audio(request):
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
                _, temp_video_path = tempfile.mkstemp(suffix='.mp4')
                with open(temp_video_path, 'wb') as temp_video:
                    temp_video.write(video_response.content)

                video = mp.VideoFileClip(temp_video_path)

                # Вибираємо аудіодоріжку з відео
                audio = video.audio

                # Зберігаємо аудіо у форматі mp3
                _, temp_audio_path = tempfile.mkstemp(suffix='.mp3')
                audio.write_audiofile(temp_audio_path, bitrate='320k')

                with open(temp_audio_path, 'rb') as f:
                    audio_data = f.read()

                response = HttpResponse(audio_data, content_type='audio/mpeg')
                response['Content-Disposition'] = f'attachment; filename="audio.mp3"'
                return response

        return HttpResponse("Reload page and try again")
