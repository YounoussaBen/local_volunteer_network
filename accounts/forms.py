# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, VolunteerProfile, OrganizationProfile, Skill, Interest, AVAILABILITY_CHOICES

class UserRegistrationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        
        return user

class UserProfileForm(forms.ModelForm):
    """Form for updating basic user profile information"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class VolunteerProfileForm(forms.ModelForm):
    """Form for volunteer-specific profile information"""
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    availability = forms.MultipleChoiceField(
        choices=AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = VolunteerProfile
        fields = ['skills', 'interests', 'availability']
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        
        if instance:
            # If editing an existing profile, set initial availability values
            initial = kwargs.get('initial', {})
            if instance.availability:
                initial['availability'] = instance.get_availability()
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        if commit:
            profile.save()
            
            # Set skills and interests (these are ManyToMany fields)
            self.save_m2m()
            
            # Handle the availability field separately
            profile.set_availability(self.cleaned_data.get('availability', []))
            profile.save()
        
        return profile

class OrganizationProfileForm(forms.ModelForm):
    """Form for organization-specific profile information"""
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Areas of Focus"
    )
    
    class Meta:
        model = OrganizationProfile
        fields = ['organization_name', 'mission', 'website', 'interests']
        widgets = {
            'mission': forms.Textarea(attrs={'rows': 3}),
        }