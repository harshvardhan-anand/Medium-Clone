# Generated by Django 3.1.5 on 2021-01-29 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210127_1739'),
        ('user_info', '0006_auto_20210129_0020'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='loginhistory',
            options={'verbose_name_plural': 'Login Histories'},
        ),
        migrations.AddField(
            model_name='profile',
            name='bookmark',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='blog.Post'),
        ),
    ]
