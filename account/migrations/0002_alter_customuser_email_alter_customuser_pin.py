# Generated by Django 4.0.3 on 2022-04-14 02:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='pin',
            field=models.PositiveIntegerField(default=111111, validators=[django.core.validators.MaxValueValidator(999999)]),
        ),
    ]
