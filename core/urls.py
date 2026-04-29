from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Порожній шлях '' означає головну сторінку (наприклад, 127.0.0.1:8000/)
    path('', views.welcome_page, name='welcome'),
    path('ptsdinfo/', views.ptsd_info, name='ptsdinfo'),
]