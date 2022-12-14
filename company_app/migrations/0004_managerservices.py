# Generated by Django 4.1.2 on 2022-11-27 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company_app', '0003_notifications_delete_managerservices'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagerServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=250, null=True)),
                ('paid_amount', models.CharField(max_length=250, null=True)),
                ('discription', models.TextField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('documents', models.JSONField(blank=True, default=dict)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
