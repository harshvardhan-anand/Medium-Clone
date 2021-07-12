from .models import Activity

def create_activity(user, action=None, target=None, action_type=None):
    Activity.objects.create(
        user = user,
        action = action,
        target = target,
        action_type = action_type
    )