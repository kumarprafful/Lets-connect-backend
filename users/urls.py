from django.urls import path
from users import views

urlpatterns = [
    path('contacts/', views.fetch_contact_list, name='contacts'),
    path('update/', views.update_customer_info, name='update'),


]