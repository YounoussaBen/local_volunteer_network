# opportunities/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Opportunity management
    path('', views.opportunity_list, name='opportunity_list'),
    path('create/', views.create_opportunity, name='create_opportunity'),
    path('<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('<int:pk>/edit/', views.edit_opportunity, name='edit_opportunity'),
    path('<int:pk>/delete/', views.delete_opportunity, name='delete_opportunity'),
    
    # Application management
    path('<int:pk>/apply/', views.apply_opportunity, name='apply_opportunity'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/<int:pk>/update/', views.update_application, name='update_application'),
    
    # Feedback
    path('applications/<int:pk>/feedback/', views.add_feedback, name='add_feedback'),
]