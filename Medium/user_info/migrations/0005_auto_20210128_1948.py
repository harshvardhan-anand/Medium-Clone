# Generated by Django 3.1.5 on 2021-01-28 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0004_loginhistory_is_in_european_union'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginhistory',
            old_name='continent',
            new_name='continent_name',
        ),
    ]