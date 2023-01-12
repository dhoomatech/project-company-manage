# Generated by Django 4.1.2 on 2022-12-25 16:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_manage', '0009_alter_loginuser_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='expiry_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='loginuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]