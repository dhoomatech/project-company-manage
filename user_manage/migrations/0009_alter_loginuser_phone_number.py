# Generated by Django 4.1.2 on 2022-11-27 08:12

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0008_employeedetails_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='phone_number',
            field=phone_field.models.PhoneField(max_length=31, unique=True),
        ),
    ]
