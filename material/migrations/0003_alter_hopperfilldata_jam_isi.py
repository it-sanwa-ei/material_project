# Generated by Django 4.0.3 on 2022-04-14 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0002_alter_hopperfilldata_jam_isi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hopperfilldata',
            name='jam_isi',
            field=models.TimeField(default='09:18', verbose_name='jam_isi'),
        ),
    ]