# Generated by Django 2.2.3 on 2019-08-04 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadfiles',
            name='file_type',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
