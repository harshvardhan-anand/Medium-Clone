# Generated by Django 3.1.5 on 2021-01-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0003_auto_20210128_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='loginhistory',
            name='is_in_european_union',
            field=models.BooleanField(null=True),
        ),
    ]
