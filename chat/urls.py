from django.urls import path
from chat import views

urlpatterns = [
    path('', views.index, name='index'),
    path('messages/', views.initial_messages, name='initial-messages'),
]