# Generated by Django 3.2 on 2023-01-26 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_app', '0007_filemanager_expiry_date_filemanager_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='filemanager',
            name='file_name',
            field=models.CharField(max_length=250, null=True),
        ),
    ]