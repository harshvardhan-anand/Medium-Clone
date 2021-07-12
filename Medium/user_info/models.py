from django.db import models
from django.conf import settings
from blog.models import Tag
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.auth.models import User
from blog.models import Post
# Create your models here.


class Person(User):
    class Meta:
        proxy=True

    def get_absolute_url(self):
        return reverse_lazy('user_info:authorbio', kwargs={"username": self.username})
        
class LoginHistory(models.Model):
    # for null we are using 0
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='history')
    login = models.DateTimeField(auto_now_add=True, verbose_name="Login Date")
    ip = models.GenericIPAddressField(null=True, verbose_name="Login IP")
    city = models.CharField(max_length=70, null=True)
    postal_code = models.CharField(max_length=70, null=True)
    longitude = models.FloatField(default=0.0, null=True)
    latitude = models.FloatField(default=0.0, null=True)
    country_name = models.CharField(max_length=50, null=True)
    country_code = models.CharField(max_length=10, null=True)
    continent_name = models.CharField(max_length=70, null=True)
    continent_code = models.CharField(max_length=10, null=True)
    timezone = models.CharField(max_length=100, null=True)
    is_in_european_union = models.BooleanField(null=True)
    device = models.CharField(max_length=50, null=True) #type of device - mobile desktop
    user_agent = models.TextField(blank=True)

    # https://stackoverflow.com/a/8369031
    class Meta:
        verbose_name_plural = 'Login Histories'

    def __str__(self):
        return f"{self.user}"

class Activity(models.Model):
    ACTION_TYPE = (
        ('post', 'POST'),
        ('follow', 'FOLLOW')
    )
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='activities')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('content_type', 'object_id')
    action = models.CharField(max_length=200)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.action} {self.target}"
        
class Profile(models.Model):
    MEMBERSHIP_STATUS = (
        (False, "Become a member"),
        (True, 'Already a member')
    )
    user = models.OneToOneField(Person, on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True)
    membership = models.BooleanField(default=False, verbose_name="Membership Status")
    expiry = models.DateTimeField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='profiles', blank=True)
    updated = models.DateTimeField(auto_now=True)
    following = models.ManyToManyField(Person, blank=True, symmetrical=False, related_name='followers')
    bookmark = models.ManyToManyField(Post, blank=True, symmetrical=False, related_name='profiles')
    activity = GenericRelation(Activity, related_query_name='profile')

    def __str__(self):
        return f"{self.user}"
    

class Membership(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    braintree_id = models.CharField(max_length=200)
    created = models.DateTimeField(verbose_name="Membership Created")
    expiry = models.DateTimeField(null=True)