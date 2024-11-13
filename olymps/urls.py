from django.urls import path

from . import views

app_name = 'olymps'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:olymp_id>/', views.detail, name='detail'),
    path('<int:olymp_id>/edit', views.edit, name='edit'),
    # path('add/', views.add, name='add'),
    # path('add_submit/', views.add_submit, name='add_submit'),
    path('<int:olymp_id>/<int:stage_id>/delete', views.stage_delete, name='stage_delete'),
    path('<int:olymp_id>/stage_add', views.stage_add, name='stage_add'),
]