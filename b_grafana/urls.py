from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='app'),
    path('about/', views.about, name='app-about'),
]