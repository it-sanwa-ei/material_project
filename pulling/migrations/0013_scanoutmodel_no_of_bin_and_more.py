# Generated by Django 4.0.3 on 2022-06-30 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulling', '0012_scaninmodel_scanoutmodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanoutmodel',
            name='no_of_bin',
            field=models.IntegerField(blank=True, null=True, verbose_name='No of bin'),
        ),
        migrations.AddField(
            model_name='temppullingscanoutmodel',
            name='no_of_bin',
            field=models.IntegerField(blank=True, null=True, verbose_name='No of bin'),
        ),
    ]