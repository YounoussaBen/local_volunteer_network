# accounts/admin.py

from django.contrib import admin
from .models import UserProfile, VolunteerProfile, OrganizationProfile, Skill, Interest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'address')
    date_hierarchy = 'created_at'

@admin.register(VolunteerProfile)
class VolunteerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'get_availability_display')
    filter_horizontal = ('skills', 'interests')
    search_fields = ('user_profile__user__username', 'user_profile__user__email')
    
    def get_username(self, obj):
        return obj.user_profile.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user_profile__user__username'
    
    def get_email(self, obj):
        return obj.user_profile.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user_profile__user__email'

@admin.register(OrganizationProfile)
class OrganizationProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'get_email', 'website', 'is_verified')
    list_filter = ('is_verified',)
    search_fields = ('organization_name', 'user_profile__user__email', 'website')
    filter_horizontal = ('interests',)
    
    def get_email(self, obj):
        return obj.user_profile.user.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user_profile__user__email'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')