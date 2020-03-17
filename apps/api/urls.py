from django.conf.urls import url, include
from django.urls import path

app_name = 'Api'

urlpatterns = [
    path('youtube/', include('apps.youtube.urls', 'youtube-api')),
]
