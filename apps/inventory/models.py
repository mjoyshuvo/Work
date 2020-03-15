from django.db import models
from apps.common.models import CompanyDomain
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class InventoryType(CompanyDomain):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=50)
    code = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['company', 'code'], ['company', 'name']]

    def __str__(self):
        return "{}-{}".format(self.name, self.company)


class Inventory(CompanyDomain):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=50)
    type = models.ForeignKey(InventoryType, null=False, blank=False, related_name='inventoryType', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    reorder_level = models.PositiveIntegerField(null=False, blank=False)
    count = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(choices=(
        ('unit', 'Unit'), ('kg', 'KG'), ('gm', 'Gram'), ('mg', 'Mili Gram'), ('ltr', 'Liter'), ('cm', 'Centimetre'),
        ('meter', 'Meter')),
        null=False,
        blank=False, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['company', 'name']


""" Audit Log Register """
auditlog.register(InventoryType)
auditlog.register(Inventory)
