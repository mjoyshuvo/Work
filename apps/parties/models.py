from django.db import models
from apps.common.models import Banks


class CustomerCategory(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Customers(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    category = models.ForeignKey(CustomerCategory, null=False, blank=False, related_name='customer_category',
                                 on_delete=models.PROTECT)
    sub_type = models.IntegerField(choices=((1, 'Individual'), (2, 'Organization')), null=False, blank=False)
    opening_balance = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100, default=0.00)
    code = models.CharField(null=True, blank=True, max_length=20)
    pin_number = models.CharField(null=True, blank=True, max_length=6)
    email = models.EmailField(null=False, blank=False, unique=True)
    nationality = models.CharField(null=True, blank=True, max_length=50)
    mobile = models.CharField(null=False, blank=False, max_length=14)
    description = models.TextField(null=True, blank=True)
    founded_on = models.DateField(null=True, blank=True)
    registration_no = models.CharField(null=True, blank=True, max_length=20)
    vat_registration_no = models.CharField(null=True, blank=True, max_length=20)
    relationship = models.CharField(choices=(
        ('individual', 'Idividual'), ('B2B', 'Business 2 Business'),
        ('B2P', 'Business 2 Person'), ('P2P', 'Person 2 Person'),
        ('P2B', 'Person 2 Business')), null=False, blank=False, default='B2B', max_length=10)
    billing_address = models.TextField(null=False, blank=False)
    shipping_address = models.TextField(null=False, blank=False)
    bank = models.ForeignKey(Banks, null=False, blank=False, on_delete=models.PROTECT)
    account_name = models.CharField(null=True, blank=True, max_length=100)
    account_number = models.CharField(null=True, blank=True, max_length=50)
    contact_person_name = models.CharField(null=False, blank=False, max_length=30)
    contact_person_mobile = models.CharField(null=False, blank=False, max_length=14)
    contact_person_email = models.EmailField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)


class VendorCategory(models.Model):
    name = models.CharField(null=False, blank=False, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Vendors(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    category = models.ForeignKey(VendorCategory, null=False, blank=False, related_name='category',
                                 on_delete=models.PROTECT)
    sub_type = models.IntegerField(choices=((1, 'Individual'), (2, 'Organization')), null=False, blank=False)
    opening_balance = models.DecimalField(decimal_places=2, null=True, blank=True, max_digits=100, default=0.00)
    code = models.CharField(null=True, blank=True, max_length=20)
    pin_number = models.CharField(null=True, blank=True, max_length=6)
    email = models.EmailField(null=False, blank=False, unique=True)
    nationality = models.CharField(null=True, blank=True, max_length=50)
    mobile = models.CharField(null=False, blank=False, max_length=14)
    description = models.TextField(null=True, blank=True)
    founded_on = models.DateField(null=True, blank=True)
    registration_no = models.CharField(null=True, blank=True, max_length=20)
    vat_registration_no = models.CharField(null=True, blank=True, max_length=20)
    relationship = models.CharField(choices=(
        ('individual', 'Idividual'), ('B2B', 'Business 2 Business'),
        ('B2P', 'Business 2 Person'), ('P2P', 'Person 2 Person'),
        ('P2B', 'Person 2 Business')), null=False, blank=False, default='B2B', max_length=10)
    billing_address = models.TextField(null=False, blank=False)
    shipping_address = models.TextField(null=False, blank=False)
    bank = models.ForeignKey(Banks, null=False, blank=False, on_delete=models.PROTECT)
    account_name = models.CharField(null=True, blank=True, max_length=100)
    account_number = models.CharField(null=True, blank=True, max_length=50)
    account_start_date = models.DateField(null=True, blank=True)
    contact_person_name = models.CharField(null=False, blank=False, max_length=30)
    contact_person_mobile = models.CharField(null=False, blank=False, max_length=14)
    contact_person_email = models.EmailField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.name)
