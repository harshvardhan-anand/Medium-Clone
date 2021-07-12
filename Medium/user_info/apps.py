from django.apps import AppConfig


class UserInfoConfig(AppConfig):
    name = 'user_info'

    def ready(self):
        from . import signals