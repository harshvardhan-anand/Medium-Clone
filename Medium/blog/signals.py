# https://docs.djangoproject.com/en/3.1/ref/signals/#m2m-changed

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from django.http import request
from django.db.models.signals import post_save
from django.dispatch import Signal
from user_info.utils import create_activity
from django.utils import timezone


# We will use action argument to check whether signal is pre_save or post_save
# https://docs.djangoproject.com/en/3.0/ref/signals/#:~:text=arguments%20sent%20to%20a%20m2m_changed%20handler

# receiver
def create_profile(**kwargs):
    Profile = kwargs.get('sender')
    Profile.objects.get_or_create(user=kwargs.get('user'))
    create_activity(
        user=kwargs.get('user'),
        action = 'created post',
        target = kwargs.get('target'),
        action_type = 'post'
    )
    # print(kwargs.get('user'))


profile_create_signal = Signal()  #signal
profile_create_signal.connect(create_profile, dispatch_uid="create_profile")