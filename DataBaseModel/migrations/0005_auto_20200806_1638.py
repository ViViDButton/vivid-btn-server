# Generated by Django 3.0.8 on 2020-08-06 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBaseModel', '0004_auto_20200803_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='voice',
            name='hot',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voice',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
