from django.urls import path

from . import views

app_name = 'students'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:student_id>/', views.detail, name='detail'),
    path('<int:student_id>/edit', views.edit, name='edit'),
    path('<int:student_id>/edit_submit', views.edit_submit, name='edit_submit'),
    path('add/', views.add, name='add'),
    path('add_submit/', views.add_submit, name='add_submit'),
    path('add_file/', views.add_file, name='add_file'),
    path('add_file_preview/', views.add_file_preview, name='add_file_preview'),
    path('add_file_submit/', views.add_file_submit, name='add_file_submit'),
    path('add_file_error/', views.add_file_error, name='add_file_error'),
]