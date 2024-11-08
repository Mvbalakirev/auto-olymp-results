from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/', views.detail, name='detail'),
    path('<int:student_id>/edit', views.edit, name='edit'),
    path('add/', views.add, name='add'),
    path('add_file/', views.add_file, name='add_file'),
    path('add_file_preview/', views.add_file, name='add_file_preview'),
]