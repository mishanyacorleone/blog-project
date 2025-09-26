from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('save-preferences/', views.save_preferences, name='save-preferences')
]
