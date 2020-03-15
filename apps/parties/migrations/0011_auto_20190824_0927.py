# Generated by Django 2.2.3 on 2019-08-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0010_auto_20190824_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customers',
            name='opening_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100, null=True),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='opening_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=100, null=True),
        ),
    ]
