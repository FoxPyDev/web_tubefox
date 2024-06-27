from django.shortcuts import render, HttpResponse, HttpResponseRedirect
import requests
from tubefox import TubeFox
from tubefox.yt_app_version_updater import get_yt_app_latest_version
from tubefox.subtitles import Subtitles
from django.http import StreamingHttpResponse


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
                           [max(yt_object.app_collected_data.collect_muted_video_links().keys())]['url'],
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
                           'download_audio': yt_object.app_collected_data.collect_audio_links()
                           [max(yt_object.app_collected_data.collect_audio_links().keys())],
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
        print(video_url)

        # Obtain the total size of the video stream using a HEAD request
        response = requests.head(video_url)
        if response.status_code == 200:
            total_size = int(response.headers.get('Content-Length', 0))

            chunk_size = 10 * 1024 * 1024  # Chunk size in bytes (10 MB)
            bytes_downloaded = 0  # Counter for downloaded bytes

            def stream_video():
                nonlocal bytes_downloaded
                retries = 5  # Number of retries for each chunk
                while bytes_downloaded < total_size:
                    start = bytes_downloaded
                    end = min(bytes_downloaded + chunk_size - 1, total_size - 1)
                    headers = {'Range': f'bytes={start}-{end}'}
                    success = False

                    for attempt in range(retries):
                        response = requests.get(video_url, headers=headers, stream=True)
                        if response.status_code == 206:
                            success = True
                            break
                        else:
                            print(f"Attempt {attempt + 1} failed with status code {response.status_code}")

                    if not success:
                        print("Failed to download the chunk after several attempts")
                        return

                    for chunk in response.iter_content(chunk_size=4096):
                        yield chunk

                    bytes_downloaded += end - start + 1
                    print(f"Downloaded {bytes_downloaded} bytes")

            response = StreamingHttpResponse(stream_video(), content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="output.mp4"'
            response['Content-Length'] = str(total_size)

            return response
        else:
            return HttpResponseRedirect('/bootstrap')
    else:
        return HttpResponseRedirect('/bootstrap')

# def download_muted_video(request):
#     if request.method == "POST":
#         video_url = request.POST.get('download_muted_video')
#         print(video_url)
#         headers = {
#             'Content-Type': 'application/json',
#             'User-Agent': f'com.google.android.youtube/{get_yt_app_latest_version()} (Linux; U; Android 12; GB) gzip'
#         }
#         video_response = requests.get(video_url, stream=True, headers=headers)
#
#         if video_response.status_code == 200 and 'Content-Length' in video_response.headers:
#             content_length = int(video_response.headers['Content-Length'])
#             if content_length > 0:
#                 response = StreamingHttpResponse(
#                     (chunk for chunk in video_response.iter_content(chunk_size=8192)),
#                     content_type='video/mp4'
#                 )
#                 response['Content-Disposition'] = 'attachment; filename="muted_video.mp4"'
#                 return response
#
#         return HttpResponse("Reload page and try again")

def download_muted_video(request):
    if request.method == "POST":
        # Отримуємо заголовок Content-Length, щоб дізнатися загальний розмір стріму
        response = requests.head('download_muted_video')
        total_size = int(response.headers.get('Content-Length', 0))

        chunk_size = 10 * 1024 * 1024  # Розмір частини у байтах (тут 10 МБ)
        bytes_downloaded = 0  # Лічильник завантажених байт

        # Запити частин стріму і запис у файл 'output.mp4'
        with open(f'output.webm', 'wb') as f:
            while bytes_downloaded < total_size:
                start = bytes_downloaded
                end = min(bytes_downloaded + chunk_size - 1, total_size - 1)
                headers = {'Range': f'bytes={start}-{end}'}
                response = requests.get('download_muted_video', headers=headers, stream=True)

                for chunk in response.iter_content(chunk_size=4096):
                    f.write(chunk)

                bytes_downloaded += end - start + 1
                print(f"Downloaded {bytes_downloaded} bytes")

        return HttpResponse("Download complete. Check 'output.mp4' file.")
    else:
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
                           'download_audio': yt_object.app_collected_data.collect_audio_links()
                           [max(yt_object.app_collected_data.collect_audio_links().keys())],
                           'status': 'ok'}
                          )
        except:
            return render(request, 'audio.html',
                          {'status': 'no info'})
    elif request.method == "GET":
        return render(request, 'audio.html')


def download_audio(request):
    if request.method == "POST":
        audio_url = request.POST.get('download_audio')
        print(audio_url)

        try:
            # Obtain the total size of the audio stream using a HEAD request
            response = requests.head(audio_url)
            if response.status_code == 200:
                total_size = int(response.headers.get('Content-Length', 0))

                chunk_size = 10 * 1024 * 1024  # Chunk size in bytes (10 MB)
                bytes_downloaded = 0  # Counter for downloaded bytes

                def stream_audio():
                    nonlocal bytes_downloaded
                    while bytes_downloaded < total_size:
                        start = bytes_downloaded
                        end = min(bytes_downloaded + chunk_size - 1, total_size - 1)
                        headers = {'Range': f'bytes={start}-{end}'}
                        response = requests.get(audio_url, headers=headers, stream=True)
                        print(response.status_code)
                        for chunk in response.iter_content(chunk_size=4096):
                            yield chunk

                        bytes_downloaded += end - start + 1
                        print(f"Downloaded {bytes_downloaded} bytes")

                response = StreamingHttpResponse(stream_audio(), content_type='audio/opus')
                response['Content-Disposition'] = 'attachment; filename="audio_output.opus"'
                response['Content-Length'] = str(total_size)

                return response
            else:
                return HttpResponseRedirect('/audio')  # Redirect if HEAD request fails
        except Exception as e:
            print(f"Error downloading audio: {e}")
            return HttpResponseRedirect('/audio')  # Redirect on error
    else:
        return HttpResponseRedirect('/audio')  # Redirect if not POST request


