# Generated by Django 3.1.5 on 2021-01-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0005_auto_20210128_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginhistory',
            name='latitude',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='loginhistory',
            name='longitude',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
