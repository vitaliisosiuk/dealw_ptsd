from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('ptsdinfo/', views.ptsd_info, name='ptsdinfo'),
]