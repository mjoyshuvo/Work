from django.db import models
from auditlog.registry import auditlog
from auditlog.models import AuditlogHistoryField


class Banks(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(null=False, blank=False, max_length=50)
    address = models.CharField(null=False, blank=False, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class Company(models.Model):
    history = AuditlogHistoryField()
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyDomain(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class UploadFiles(models.Model):
    file = models.FileField(upload_to='imported_files')
    file_type = models.CharField(null=False, blank=False, default=None, max_length=20,
                                 choices=(('sales-order', 'Sales Order'), ("customer", 'Customer'), ("item", 'Item'),
                                          ("price_declaration", 'Price Declaration'), ("stock", 'Stock'),
                                          ("vendor", 'Vendor')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


""" Audit Log Register """
auditlog.register(Banks)
auditlog.register(Company)
