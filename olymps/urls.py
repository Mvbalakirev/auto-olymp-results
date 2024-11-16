from django.urls import path

from . import views

app_name = 'olymps'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:olymp_id>/', views.detail, name='detail'),
    path('<int:olymp_id>/edit/', views.edit, name='edit'),
    # path('add/', views.add, name='add'),
    path('<int:olymp_id>/<int:stage_num>/', views.stage_detail, name='stage_detail'),
    path('<int:olymp_id>/<int:stage_id>/', views.stage_detail, name='stage_detail_by_id'),
    path('<int:olymp_id>/<int:stage_id>/delete/', views.stage_delete, name='stage_delete'),
    path('<int:olymp_id>/stage_add/', views.stage_add, name='stage_add'),
]