from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('singers/', views.singer_list),
    path('singers/<int:pk>/', views.singer_detail),
    path('singers/<int:singer_id>/songs/', views.song_create),
    path('songs/<int:song_id>/comments/', views.comment_list),
    path('songs/<int:song_id>/comments/new/', views.comment_create),
]
