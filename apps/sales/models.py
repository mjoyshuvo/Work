from django.db import models
from apps.product_and_service.models import Service
from apps.parties.models import Customers, Vendors
import uuid
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class DummyServicePurchased(models.Model):
    product_name = models.CharField(null=False, blank=False, max_length=100)
    unit_type = models.CharField(null=False, blank=False, max_length=10)
    quantity = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50)
    per_unit_price = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50)
    unit_total = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50)
    subsidiary_vat = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    vat_per_unit = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    vat_amount = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    price_after_vat = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SalesInvoice(models.Model):
    history = AuditlogHistoryField()
    invoice_number = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, unique=True)
    approved = models.BooleanField(default=False, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Sales(models.Model):
    history = AuditlogHistoryField()
    invoice = models.ForeignKey(SalesInvoice, null=False, blank=False, related_name='sales',
                                on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=False, blank=False, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customers, null=False, blank=False, on_delete=models.PROTECT)
    quantity = models.DecimalField(decimal_places=2, null=False, blank=False, max_digits=50)
    per_unit_price = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50)
    unit_total = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50)
    subsidiary_vat = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    vat_per_unit = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    vat_amount = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    price_after_vat = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=50, default=0.00)
    order_date = models.DateField(null=False, blank=False)
    approved = models.BooleanField(null=False, blank=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


""" Audit Log Register """
auditlog.register(SalesInvoice)
auditlog.register(Sales)
