from django.urls import path

from . import views

app_name = 'olymps'
urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:olymp_id>/', views.detail, name='detail'),
    # path('<int:olymp_id>/edit', views.edit, name='edit'),
    # path('<int:olymp_id>/edit_submit', views.edit_submit, name='edit_submit'),
    # path('add/', views.add, name='add'),
    # path('add_submit/', views.add_submit, name='add_submit'),
]