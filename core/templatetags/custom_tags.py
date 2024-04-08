# core/templatetags/custom_tags.py

from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter
def get_dict_item(dictionary, key):
    """Get an item from a dictionary by key"""
    return dictionary.get(key)

@register.filter
def status_badge_class(status):
    """Return appropriate Bootstrap badge class for a status"""
    status_classes = {
        'active': 'success',
        'filled': 'warning',
        'completed': 'primary',
        'cancelled': 'secondary',
        'pending': 'info',
        'accepted': 'success',
        'declined': 'danger',
        'withdrawn': 'secondary',
    }
    return status_classes.get(status.lower(), 'secondary')

@register.simple_tag
def url_replace(request, field, value):
    """Replace a parameter in the current URL"""
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def url_add_to_list(request, field, value):
    """Add a value to a list parameter in the current URL"""
    dict_ = request.GET.copy()
    # Get current list of values
    current_list = dict_.getlist(field)
    
    # Add value if not already present
    if value not in current_list:
        dict_.appendlist(field, value)
    
    return dict_.urlencode()

@register.simple_tag
def url_remove_from_list(request, field, value):
    """Remove a value from a list parameter in the current URL"""
    dict_ = request.GET.copy()
    
    # Get current list and remove value
    current_list = dict_.getlist(field)
    if value in current_list:
        current_list.remove(value)
    
    # Clear current values and add the updated list
    dict_.pop(field, None)
    for val in current_list:
        dict_.appendlist(field, val)
    
    return dict_.urlencode()

@register.filter
def format_date_range(start_date, end_date):
    """Format a date range nicely"""
    if not end_date or start_date == end_date:
        return start_date.strftime("%B %d, %Y")
    
    # Same month and year
    if start_date.month == end_date.month and start_date.year == end_date.year:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%d, %Y')}"
    
    # Same year
    if start_date.year == end_date.year:
        return f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
    
    # Different years
    return f"{start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')}"

@register.filter
def format_time_range(start_time, end_time):
    """Format a time range nicely"""
    if not start_time or not end_time:
        return "Time not specified"
    
    start_str = start_time.strftime("%I:%M %p")
    end_str = end_time.strftime("%I:%M %p")
    
    return f"{start_str} - {end_str}"

@register.filter
def days_until(date):
    """Calculate days until a future date"""
    if not date:
        return None
    
    now = timezone.now().date()
    
    if date < now:
        return -1  # Date has passed
    
    delta = date - now
    return delta.days

@register.filter
def days_status(days):
    """Return appropriate status for days remaining"""
    if days is None:
        return ''
    
    if days < 0:
        return 'expired'
    elif days == 0:
        return 'today'
    elif days <= 3:
        return 'urgent'
    else:
        return 'upcoming'