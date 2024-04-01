# opportunities/admin.py

from django.contrib import admin
from .models import Opportunity, Application

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'location', 'start_date', 'positions', 'positions_filled', 'status')
    list_filter = ('status', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'location', 'organization__organization_name')
    filter_horizontal = ('required_skills', 'interests')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'organization')
        }),
        ('Details', {
            'fields': ('location', 'start_date', 'end_date', 'start_time', 'end_time')
        }),
        ('Requirements', {
            'fields': ('required_skills', 'interests', 'positions', 'application_deadline')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'volunteer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('opportunity__title', 'volunteer__user_profile__user__username', 'message')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Application', {
            'fields': ('opportunity', 'volunteer', 'message', 'status')
        }),
        ('Feedback', {
            'fields': ('organization_feedback', 'volunteer_feedback')
        }),
        ('Ratings', {
            'fields': ('organization_rating', 'volunteer_rating')
        }),
    )