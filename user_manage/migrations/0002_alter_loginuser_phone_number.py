# Generated by Django 4.1.2 on 2022-10-25 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='phone_number',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
