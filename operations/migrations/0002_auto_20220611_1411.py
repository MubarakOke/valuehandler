# Generated by Django 3.2 on 2022-06-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='e_duty',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tariff',
            name='levy',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]