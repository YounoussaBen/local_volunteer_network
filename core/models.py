# core/models.py

from django.db import models

class Feedback(models.Model):
    """General feedback about the platform"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.name}: {self.subject}"

class FAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.question