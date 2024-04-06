"""
URL configuration for web_tubefox project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base_app.views import index_page, bootstrap_page, download_video

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page),
    path('about/', index_page, name='about'),
    path('contact/', index_page, name='contact'),
    path('video/', index_page, name='video'),
    path('thumbnail/', index_page, name='thumbnail'),
    path('audio/', index_page, name='audio'),
    path('subtitles/', index_page, name='subtitles'),
    path('metadata/', index_page, name='metadata'),
    path('bootstrap/', bootstrap_page, name='bootstrap'),
    path('download_video/', download_video, name='download_video'),
]
