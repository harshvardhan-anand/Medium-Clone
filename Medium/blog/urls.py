from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Home.as_view(), name='Home'),
    path('<str:author>/<int:pk>/<slug:slug>', views.PostDetail.as_view(), name='post_detail'),
    path('tags/<str:tag>',views.TagRelatedPost.as_view(), name='TagRelatedPost'),
    path('pdf/<str:post>', views.PrintToPDF.as_view(), name='pdf'),
    path('t', views.test, name='test')
]
