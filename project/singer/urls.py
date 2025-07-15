from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('singers/', views.singer_list_create, name='singer_list_create'),
    path('singers/<int:singer_id>/', views.singer_detail_update_delete, name='singer_detail_update_delete'),
    path('songs/<int:singer_id>/create/', views.song_create, name='song_create'),
    path('comments/<int:song_id>/', views.comment_read_create, name='comment_read_create'),
    path('find_tag/<str:tags_name>/', views.find_tag, name='find_tag'),
]
