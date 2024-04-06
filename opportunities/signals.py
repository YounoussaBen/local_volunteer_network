# opportunities/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application

@receiver(post_save, sender=Application)
def update_opportunity_status_on_application_change(sender, instance, **kwargs):
    """Update opportunity status when an application status changes"""
    instance.opportunity.update_status()