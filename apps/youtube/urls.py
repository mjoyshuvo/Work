from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
app_name = 'youtube'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls))
]
