from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('salary', views.salary, name='salary'),
    path('hours', views.hours, name='hours'),
    path('total', views.total, name='total'),
]