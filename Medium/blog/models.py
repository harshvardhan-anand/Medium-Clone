# When using UUID with taggit, we will get "DataError:Integer out of range" error and can be fixed
# by the given link so we will not use taggit
# https://stackoverflow.com/a/33771570

import uuid
from django.shortcuts import reverse
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=20)

    def __str__(self):
        return self.tag

class Post(models.Model):
    post_id = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    body = models.TextField()
    slug = models.SlugField(unique=False)
    status = models.CharField(max_length=50,
        choices=(
            ('published', 'PUBLISHED'),
            ('draft', 'DRAFT')
        ))
    author = models.ForeignKey('user_info.Person', on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_claps = models.PositiveIntegerField(default=0, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts',blank=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'author':self.author,"pk": self.pk, 'slug':self.slug})
    

# How to use related_name in abstract classes
# https://docs.djangoproject.com/en/3.1/topics/db/models/#be-careful-with-related-name-and-related-query-name
# last s is to create plural name in "%(class)ss"
class BaseId(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)ss')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='%(class)ss')
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class Clap(BaseId):
    # Django set range for integer model field as constraint
    # https://stackoverflow.com/a/33773128
    claps_given = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(50), MinValueValidator(1)]
    )


class Comment(BaseId):
    comment = models.TextField()