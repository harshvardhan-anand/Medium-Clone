# Generated by Django 3.1.5 on 2021-01-30 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0010_auto_20210130_2313'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='country',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='device',
        ),
    ]