# Generated by Django 4.0.3 on 2022-06-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pulling', '0006_pullingfinishgooditem'),
    ]

    operations = [
        migrations.AddField(
            model_name='pullingfinishgooditem',
            name='total_quantity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Total Quantity'),
        ),
    ]