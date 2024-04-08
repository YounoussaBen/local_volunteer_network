# core/context_processors.py

from accounts.models import Skill, Interest

def global_settings(request):
    """Add global settings to context"""
    return {
        'SITE_NAME': 'Local Volunteer Network',
        'SITE_DESCRIPTION': 'Connecting volunteers with opportunities in Accra',
    }

def global_data(request):
    """Add globally accessible data to templates"""
    return {
        'all_skills': Skill.objects.all(),
        'all_interests': Interest.objects.all(),
    }