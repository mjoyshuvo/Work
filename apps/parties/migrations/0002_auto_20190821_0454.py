# Generated by Django 2.2.3 on 2019-08-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='pin_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
