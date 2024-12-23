from django.contrib import admin
from django.urls import include, path
import olymps.views

urlpatterns = [
    path('students/', include('students.urls')),
    path('olymps/', include('olymps.urls')),
    path('admin/', admin.site.urls),
    path('', olymps.views.index)
]
