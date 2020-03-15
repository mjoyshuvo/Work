from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.parties.views import CustomerCategoryViewSet, CustomerViewSet, VendorCategoryViewSet, VendorViewSet
app_name = 'parties'

router = DefaultRouter()

router.register(r'customer_categories', CustomerCategoryViewSet, base_name='customer_categories')
router.register(r'customers', CustomerViewSet, base_name='customers')
router.register(r'vendor_categories', VendorCategoryViewSet, base_name='vendor_categories')
router.register(r'vendors', VendorViewSet, base_name='vendors')

urlpatterns = [
    path('', include(router.urls))
]
