# Generated by Django 4.0.3 on 2022-04-20 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_email_alter_customuser_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=25, unique=True, verbose_name='username'),
        ),
    ]
