# Generated by Django 3.2 on 2023-01-26 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0009_remove_filemanager_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemanager',
            name='expiry_date',
            field=models.IntegerField(default=0, max_length=150),
        ),
    ]
