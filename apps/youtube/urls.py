from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import VideoViewSet

app_name = 'youtube'

router = DefaultRouter()
router.register(r'videos', VideoViewSet, base_name='videos')

urlpatterns = [
    path('', include(router.urls))
]
