# Generated by Django 5.0.7 on 2024-08-06 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='normalized_name',
            field=models.CharField(default='', editable=False, max_length=255),
        ),
    ]
