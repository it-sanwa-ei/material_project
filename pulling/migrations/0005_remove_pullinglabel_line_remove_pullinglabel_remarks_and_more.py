# Generated by Django 4.0.3 on 2022-06-22 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pulling', '0004_alter_pullinglabel_line_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pullinglabel',
            name='line',
        ),
        migrations.RemoveField(
            model_name='pullinglabel',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='pullinglabel',
            name='shift_group',
        ),
        migrations.RemoveField(
            model_name='pullinglabel',
            name='tooling',
        ),
    ]