from django.urls import path
from . import views

app_name = 'assessments'


urlpatterns = [
    path('', views.test_main_view, name='all-tests'),

    path('<slug:test_slug>/', views.about_test, name='about-test'),
    path('<slug:test_slug>/take/', views.take_test, name='take-test'),
    path('<slug:test_slug>/result/', views.test_result, name='test-result'),
]