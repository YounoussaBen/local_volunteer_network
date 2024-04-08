# core/forms.py

from django import forms
from .models import Feedback

class ContactForm(forms.ModelForm):
    """Form for contact page"""
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }