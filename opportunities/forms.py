# opportunities/forms.py

from django import forms
from .models import Opportunity, Application
from accounts.models import Skill, Interest

class OpportunityForm(forms.ModelForm):
    """Form for creating and editing volunteer opportunities"""
    required_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Related Interests/Causes"
    )
    
    class Meta:
        model = Opportunity
        fields = [
            'title', 'description', 'location', 
            'start_date', 'end_date', 'start_time', 'end_time',
            'required_skills', 'interests', 'positions', 'application_deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class ApplicationForm(forms.ModelForm):
    """Form for volunteers to apply to opportunities"""
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3, 
                'placeholder': 'Explain why you are interested in this opportunity and how your skills align with the requirements.'
            }),
        }

class ApplicationStatusForm(forms.ModelForm):
    """Form for organizations to update application status"""
    class Meta:
        model = Application
        fields = ['status', 'organization_feedback']
        widgets = {
            'organization_feedback': forms.Textarea(attrs={'rows': 3}),
        }

class VolunteerFeedbackForm(forms.ModelForm):
    """Form for volunteers to provide feedback after an opportunity"""
    class Meta:
        model = Application
        fields = ['volunteer_feedback', 'volunteer_rating']
        widgets = {
            'volunteer_feedback': forms.Textarea(attrs={'rows': 3}),
            'volunteer_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'volunteer_rating': 'Rating (1-5 stars)',
        }

class OrganizationFeedbackForm(forms.ModelForm):
    """Form for organizations to provide feedback on volunteers"""
    class Meta:
        model = Application
        fields = ['organization_feedback', 'organization_rating']
        widgets = {
            'organization_feedback': forms.Textarea(attrs={'rows': 3}),
            'organization_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'organization_rating': 'Rating (1-5 stars)',
        }