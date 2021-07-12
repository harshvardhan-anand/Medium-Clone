# Generated by Django 3.1.5 on 2021-01-27 12:09

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('claps_given', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(50), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('title', models.CharField(max_length=50)),
                ('body', models.TextField()),
                ('slug', models.SlugField()),
                ('status', models.CharField(choices=[('published', 'PUBLISHED'), ('draft', 'DRAFT')], max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('total_claps', models.PositiveIntegerField(blank=True, default=0)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
    ]