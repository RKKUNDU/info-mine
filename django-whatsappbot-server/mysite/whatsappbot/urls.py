from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.Message, name='bot'),
    path('admin/', admin.site.urls),
]
