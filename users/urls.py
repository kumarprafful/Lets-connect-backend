from django.urls import path
from users import views

urlpatterns = [
    path('contacts/', views.fetch_contact_list, name='contacts'),
    path('update/', views.update_customer_info, name='update'),
    path('invite/', views.invite_friends, name='invite'),
    path('get-invites/', views.get_invites, name='get-invites'),
    path('invite-action/', views.invite_action, name='invite-action'),

]