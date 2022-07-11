# Generated by Django 4.0.3 on 2022-07-08 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pulling', '0015_alter_scanoutmodel_rack'),
    ]

    operations = [
        migrations.AddField(
            model_name='scaninmodel',
            name='pic',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='PIC'),
        ),
        migrations.AddField(
            model_name='scanoutmodel',
            name='pic',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='PIC'),
        ),
        migrations.AddField(
            model_name='temppullingscaninmodel',
            name='pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='PIC'),
        ),
        migrations.AddField(
            model_name='temppullingscanoutmodel',
            name='pic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='PIC'),
        ),
    ]
