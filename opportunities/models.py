# opportunities/models.py

from django.db import models
from accounts.models import OrganizationProfile, VolunteerProfile, Skill, Interest

class Opportunity(models.Model):
    """Model for volunteer opportunities"""
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('filled', 'Filled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    # Basic information
    title = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE, related_name='opportunities')
    
    # Details
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # Optional for one-day events
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    # Requirements
    required_skills = models.ManyToManyField(Skill, blank=True, related_name='opportunities')
    interests = models.ManyToManyField(Interest, blank=True, related_name='opportunities')
    positions = models.PositiveIntegerField(default=1)  # Number of volunteers needed
    
    # Status and management
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    application_deadline = models.DateField(null=True, blank=True)
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def positions_filled(self):
        """Return number of accepted applications"""
        return self.applications.filter(status='accepted').count()
    
    @property
    def positions_available(self):
        """Return number of available positions"""
        return self.positions - self.positions_filled
    
    @property
    def is_full(self):
        """Check if all positions are filled"""
        return self.positions_filled >= self.positions
    
    def update_status(self):
        """Update opportunity status based on filled positions"""
        if self.is_full and self.status == 'active':
            self.status = 'filled'
            self.save()

class Application(models.Model):
    """Model for volunteer applications to opportunities"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('withdrawn', 'Withdrawn'),
    )
    
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    volunteer = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='applications')
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Feedback
    organization_feedback = models.TextField(blank=True, null=True)
    volunteer_feedback = models.TextField(blank=True, null=True)
    
    # Ratings (1-5 stars)
    organization_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    volunteer_rating = models.PositiveSmallIntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ('opportunity', 'volunteer')
    
    def __str__(self):
        return f"{self.volunteer} applied to {self.opportunity}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update opportunity status when application status changes
        self.opportunity.update_status()