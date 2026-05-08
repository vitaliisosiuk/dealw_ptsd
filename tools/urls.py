from django.urls import path
from . import views

app_name = 'tools'

urlpatterns = [
    path('', views.tools_home_view, name='home'),
    path('triggers/', views.triggers_view, name='triggers'),
    path('triggers/map/', views.trigger_mapping_view, name='trigger_map'),
    path('triggers/summary/<int:log_id>/', views.trigger_summary_view, name='trigger_summary'),
    path('inspirational-cards/', views.inspirational_cards_info_view, name='inspirational_cards_info'),
    path('inspirational-cards/view/', views.inspirational_cards_view, name='inspirational_cards_view'),
    path('express-with-art/', views.express_with_art_view, name='express_with_art'),
    path('meditation/', views.meditation_view, name='meditation'),
    path('journal/', views.journal_view, name='journal'),
    path('getting-out-of-house/', views.getting_out_of_house_view, name='getting_out_of_house'),
]