from django.shortcuts import render
from base_app.models import Workers
from django.http import HttpResponse


def index_page(request):
    all_workers = Workers.objects.all()
    return render(request, 'index.html', {'data': all_workers})
