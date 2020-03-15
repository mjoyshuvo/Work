from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.product_and_service.views import ServiceItemViewSet, ServiceViewSet
app_name = 'product_and_service'

router = DefaultRouter()

router.register(r'service_item_categories', ServiceItemViewSet, base_name='service_item_categories')
router.register(r'services', ServiceViewSet, base_name='services')

urlpatterns = [
    path('', include(router.urls))
]
