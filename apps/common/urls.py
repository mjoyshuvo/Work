from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.common.views import UploadFilesViewSet, BankViewSet
app_name = 'common'

router = DefaultRouter()

router.register(r'upload_file', UploadFilesViewSet, base_name='upload_file')
router.register(r'banks', BankViewSet, base_name='banks')

urlpatterns = [
    path('', include(router.urls))
]
