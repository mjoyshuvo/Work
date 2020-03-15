from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from apps.sales.views import SupplierPurchasedViewSet, SalesViewSet, SalesInvoiceViewSet, tax_challan_report, service_invoice

app_name = 'sales'

router = DefaultRouter()

router.register(r'sales_invoice', SalesInvoiceViewSet, base_name='sales_invoice')
router.register(r'sales_list', SalesViewSet, base_name='sales_list')
router.register(r'tax_challan', SupplierPurchasedViewSet, base_name='tax_challan')

urlpatterns = [
    path('', include(router.urls)),
    url(r'^tax_challan_report/', tax_challan_report, name='tax_challan_report'),
    url(r'^service_invoice/', service_invoice, name='service_invoice'),
]
