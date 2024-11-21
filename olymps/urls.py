from django.urls import path

from . import views

app_name = 'olymps'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:olymp_id>/', views.detail, name='detail'),
    path('<int:olymp_id>/edit/', views.edit, name='edit'),
    path('<int:olymp_id>/delete/', views.delete, name='delete'),
    path('add/', views.add, name='add'),
    path('<int:olymp_id>/<int:stage_id>/', views.stage_detail, name='stage_detail'),
    path('<int:olymp_id>/<int:stage_id>/edit/', views.stage_edit, name='stage_edit'),
    path('<int:olymp_id>/<int:stage_id>/delete/', views.stage_delete, name='stage_delete'),
    path('<int:olymp_id>/stage_add/', views.stage_add, name='stage_add'),
    path('<int:olymp_id>/<int:stage_id>/', views.stage_detail, name='stage_subject_detail'),
    path('<int:olymp_id>/<int:stage_id>/edit/', views.stage_edit, name='stage_subject_edit'),
    path('<int:olymp_id>/<int:stage_id>/delete/', views.stage_delete, name='stage_subject_delete'),
    path('<int:olymp_id>/<int:stage_id>/subject_add/', views.stage_subject_add, name='stage_subject_add'),
]