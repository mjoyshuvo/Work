from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField
from django.db import models
from apps.parties.models import Vendors


# Create your models here.


class ServiceItem(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, unique=True, max_length=30)
    code = models.IntegerField(null=False, blank=False, unique=True)
    type = models.CharField(
        choices=(('On Demand Service', 'On Demand Service'), ('Recurrent Service', 'Recurrent Service')), null=False,
        blank=False, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=100)
    service_code = models.CharField(null=False, blank=False, max_length=15)
    preferred_vendor = models.ForeignKey(Vendors, null=True, blank=True, on_delete=models.PROTECT,
                                         related_name='vendor')
    description = models.TextField(null=True, blank=True)
    item_type = models.CharField(null=True, blank=True, max_length=50)
    service_item_category = models.ForeignKey(ServiceItem, null=False, blank=False, on_delete=models.PROTECT,
                                              related_name='serviceitem')
    mrp = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=100)
    sell_price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=100)
    sell_discount = models.IntegerField(null=True, blank=True, default=0)
    step_size = models.IntegerField(null=False, blank=False, default=1)
    purchase_price = models.DecimalField(null=False, blank=False, decimal_places=2, max_digits=100)
    purchase_discount = models.IntegerField(null=True, blank=True, default=0)
    unit_of_measurement = models.CharField(
        choices=(
            ('unit', 'Unit'), ('kg', 'KG'), ('gm', 'Gram'), ('mg', 'Mili Gram'), ('ltr', 'Liter'), ('cm', 'Centimetre'),
            ('meter', 'Meter')),
        null=False,
        blank=False, max_length=10)
    vat = models.IntegerField(null=True, blank=True, default=0)
    so = models.BooleanField(null=False, blank=False, default=True)
    po = models.BooleanField(null=False, blank=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


""" Audit Log Register """
auditlog.register(ServiceItem)
auditlog.register(Service)
