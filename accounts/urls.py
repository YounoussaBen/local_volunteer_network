# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Registration URLs
    path('register/', views.register, name='register'),
    path('register/volunteer/', views.register_volunteer, name='register_volunteer'),
    path('register/organization/', views.register_organization, name='register_organization'),
    
    # Profile URLs
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/edit/volunteer/', views.edit_volunteer_profile, name='edit_volunteer_profile'),
    path('profile/edit/organization/', views.edit_organization_profile, name='edit_organization_profile'),
    
    # Other account-related URLs
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('volunteers/<int:pk>/', views.volunteer_detail, name='volunteer_detail'),
    path('organizations/', views.organization_list, name='organization_list'),
    path('organizations/<int:pk>/', views.organization_detail, name='organization_detail'),
]