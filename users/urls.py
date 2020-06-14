from django.urls import path
from users import views

urlpatterns = [
    path('contacts/', views.fetch_contact_list, name='contacts'),
]