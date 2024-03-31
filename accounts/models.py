# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# User types
USER_TYPE_CHOICES = (
    ('volunteer', 'Volunteer'),
    ('organization', 'Organization'),
)

# Availability choices
AVAILABILITY_CHOICES = (
    ('weekday_morning', 'Weekday Mornings'),
    ('weekday_afternoon', 'Weekday Afternoons'),
    ('weekday_evening', 'Weekday Evenings'),
    ('weekend_morning', 'Weekend Mornings'),
    ('weekend_afternoon', 'Weekend Afternoons'),
    ('weekend_evening', 'Weekend Evenings'),
)

class UserProfile(models.Model):
    """Base profile model for all users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Skill(models.Model):
    """Skills that volunteers can have"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Interest(models.Model):
    """Interests/causes that volunteers can be interested in"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class VolunteerProfile(models.Model):
    """Extended profile for volunteer users"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='volunteer_profile')
    skills = models.ManyToManyField(Skill, blank=True, related_name='volunteers')
    interests = models.ManyToManyField(Interest, blank=True, related_name='volunteers')
    availability = models.CharField(max_length=255, blank=True, null=True)
    # Store multiple availability choices as comma-separated values
    
    def __str__(self):
        return f"{self.user_profile.user.first_name}'s Volunteer Profile"
    
    def set_availability(self, availability_list):
        """Convert list of availability choices to comma-separated string"""
        self.availability = ','.join(availability_list)
        
    def get_availability(self):
        """Convert comma-separated string to list of availability choices"""
        if not self.availability:
            return []
        return self.availability.split(',')
    
    def get_availability_display(self):
        """Get human-readable representation of availability choices"""
        if not self.availability:
            return "Not specified"
        
        avail_dict = dict(AVAILABILITY_CHOICES)
        avail_list = self.get_availability()
        return ", ".join([avail_dict.get(a, a) for a in avail_list])

class OrganizationProfile(models.Model):
    """Extended profile for organization users"""
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='organization_profile')
    organization_name = models.CharField(max_length=255)
    mission = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    interests = models.ManyToManyField(Interest, blank=True, related_name='organizations')
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.organization_name}'s Profile"

# Signals to create profiles when a user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a new user is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the user profile when the user is saved"""
    instance.profile.save()