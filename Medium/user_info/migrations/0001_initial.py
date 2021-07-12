# Generated by Django 3.1.5 on 2021-01-27 12:09

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='')),
                ('membership', models.BooleanField(default=False, verbose_name='Membership Status')),
                ('expiry', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='user_info.Person')),
                ('tags', models.ManyToManyField(blank=True, related_name='profiles', to='blog.Tag')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_info.person')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('braintree_id', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=50)),
                ('device', models.CharField(max_length=50)),
                ('created', models.DateTimeField(verbose_name='Membership History')),
                ('expiry', models.DateTimeField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_info.person')),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.DateTimeField(auto_now_add=True, verbose_name='Login Date')),
                ('longitude', models.FloatField(blank=True, default=0.0)),
                ('latitude', models.FloatField(blank=True, default=0.0)),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='Login IP')),
                ('country', models.CharField(blank=True, max_length=50)),
                ('device', models.CharField(blank=True, max_length=50)),
                ('user_agent', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='user_info.person')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_id', models.PositiveIntegerField(blank=True, null=True)),
                ('action', models.CharField(max_length=200)),
                ('action_type', models.CharField(choices=[('post', 'POST'), ('follow', 'FOLLOW')], max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('target_ct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='user_info.person')),
            ],
        ),
    ]
