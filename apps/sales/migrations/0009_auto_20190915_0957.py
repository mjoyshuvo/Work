# Generated by Django 2.2.3 on 2019-09-15 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0008_auto_20190914_0602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='invoice_number',
        ),
        migrations.DeleteModel(
            name='SalesInvoice',
        ),
    ]
