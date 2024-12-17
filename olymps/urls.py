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
    path('<int:olymp_id>/stage_add_file/', views.stage_add_file, name='stage_add_file'),
    path('<int:olymp_id>/<int:stage_id>/', views.stage_detail, name='stage_subject_detail'),
    path('<int:olymp_id>/<int:stage_id>/edit/', views.stage_edit, name='stage_subject_edit'),
    path('<int:olymp_id>/<int:stage_id>/delete/', views.stage_delete, name='stage_subject_delete'),
    path('<int:olymp_id>/<int:stage_id>/subject_add/', views.stage_subject_add, name='stage_subject_add'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/', views.stage_subject_detail, name='stage_subject_detail'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/edit/', views.stage_subject_edit, name='stage_subject_edit'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/delete/', views.stage_subject_delete, name='stage_subject_delete'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/<int:parallel>/', views.stage_subject_parallel, name='stage_subject_parallel'),

    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/application_add/', views.application_add, name='application_add'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/application_add_file/', views.application_add_file, name='application_add_file'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/application_add_file_submit/', views.application_add_file_submit, name='application_add_file_submit'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/app-<int:app_id>/edit/', views.application_edit, name='application_edit'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/app-<int:app_id>/delete/', views.application_delete, name='application_delete'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/mass_edit/', views.application_mass_edit, name='application_mass_edit'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/<int:parallel>/mass_edit/', views.application_parallel_mass_edit, name='application_parallel_mass_edit'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/<int:parallel>/grade_win_set/', views.application_parallel_grade_win_set, name='application_parallel_grade_win_set'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/<int:parallel>/add_prev_num/', views.application_parallel_add_prev_num, name='application_parallel_add_prev_num'),
    path('<int:olymp_id>/<int:stage_id>/<int:stage_subject_id>/<int:parallel>/add_prev_year/', views.application_parallel_add_prev_year, name='application_parallel_add_prev_year'),
]