from django.urls import path, include
from . import views

app_name = 'user_info'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('newUser', views.CreateUser.as_view(), name='createuser'),
    path('users/<str:username>', views.AuthorBio.as_view(), name='authorbio'), 
    path('notifications', views.Notifications.as_view(), name='notifications'), 
    path('<str:username>/membership', views.MembershipView.as_view(), name='membership')
]
