# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from .models import FAQ
from .forms import ContactForm
from opportunities.models import Opportunity, Application
from accounts.models import OrganizationProfile, VolunteerProfile, Skill, Interest
from django.utils import timezone

def home(request):
    """Home page view"""
    # Get recent opportunities for display
    recent_opportunities = Opportunity.objects.filter(status='active').order_by('-created_at')[:4]
    
    # Get counts for stats section
    volunteer_count = VolunteerProfile.objects.count()
    organization_count = OrganizationProfile.objects.count()
    opportunity_count = Opportunity.objects.count()
    application_count = Application.objects.count()
    
    context = {
        'recent_opportunities': recent_opportunities,
        'stats': {
            'volunteers': volunteer_count,
            'organizations': organization_count,
            'opportunities': opportunity_count,
            'applications': application_count
        }
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view"""
    # Get stats for about page
    volunteer_count = VolunteerProfile.objects.count()
    organization_count = OrganizationProfile.objects.count()
    opportunity_count = Opportunity.objects.count()
    application_count = Application.objects.count()
    
    # Get top skills and causes
    top_skills = Skill.objects.annotate(
        volunteer_count=Count('volunteers')
    ).order_by('-volunteer_count')[:5]
    
    top_causes = Interest.objects.annotate(
        volunteer_count=Count('volunteers')
    ).order_by('-volunteer_count')[:5]
    
    context = {
        'stats': {
            'volunteers': volunteer_count,
            'organizations': organization_count,
            'opportunities': opportunity_count,
            'applications': application_count
        },
        'top_skills': top_skills,
        'top_causes': top_causes
    }
    
    return render(request, 'core/about.html', context)

def contact(request):
    """Contact page with feedback form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you for your feedback!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})

def faq(request):
    """FAQ page view"""
    faqs = FAQ.objects.all().order_by('order')
    return render(request, 'core/faq.html', {'faqs': faqs})

@login_required
def dashboard(request):
    """User dashboard view - redirects based on user type"""
    user_profile = request.user.profile
    
    if user_profile.user_type == 'volunteer':
        # Volunteer dashboard
        # Get recommended opportunities based on skills and interests
        try:
            volunteer_profile = user_profile.volunteer_profile
            
            # Get the volunteer's skills and interests
            skills = volunteer_profile.skills.all()
            interests = volunteer_profile.interests.all()
            
            # Find matching opportunities
            recommended_opportunities = Opportunity.objects.filter(
                status='active'
            ).distinct()
            
            if skills.exists():
                recommended_opportunities = recommended_opportunities.filter(
                    required_skills__in=skills
                ).distinct()
            
            if interests.exists():
                recommended_opportunities = recommended_opportunities.filter(
                    interests__in=interests
                ).distinct()
            
            # Get the volunteer's applications
            applications = volunteer_profile.applications.all().order_by('-created_at')
            
            # Get upcoming volunteer commitments (accepted applications)
            upcoming_commitments = applications.filter(
                status='accepted',
                opportunity__status__in=['active', 'filled'],
                opportunity__start_date__gte=timezone.now().date()
            ).order_by('opportunity__start_date')[:3]
            
            # Get application stats
            application_stats = {
                'total': applications.count(),
                'pending': applications.filter(status='pending').count(),
                'accepted': applications.filter(status='accepted').count(),
                'declined': applications.filter(status='declined').count(),
                'withdrawn': applications.filter(status='withdrawn').count(),
            }
            
            context = {
                'volunteer_profile': volunteer_profile,
                'recommended_opportunities': recommended_opportunities[:5],
                'applications': applications[:5],
                'upcoming_commitments': upcoming_commitments,
                'application_stats': application_stats,
            }
            return render(request, 'accounts/volunteer_dashboard.html', context)
        
        except VolunteerProfile.DoesNotExist:
            # Volunteer profile not complete
            messages.warning(request, 'Please complete your volunteer profile to see personalized recommendations.')
            return redirect('edit_volunteer_profile')
    
    elif user_profile.user_type == 'organization':
        # Organization dashboard
        try:
            organization_profile = user_profile.organization_profile
            
            # Get the organization's opportunities
            opportunities = organization_profile.opportunities.all().order_by('-created_at')
            
            # Get recent applications
            recent_applications = []
            for opportunity in opportunities:
                applications = opportunity.applications.all().order_by('-created_at')
                recent_applications.extend(applications)
            
            # Sort by created_at and limit to 5
            recent_applications = sorted(recent_applications, key=lambda x: x.created_at, reverse=True)[:5]
            
            # Get opportunity stats
            active_opportunities = opportunities.filter(status='active').count()
            filled_opportunities = opportunities.filter(status='filled').count()
            completed_opportunities = opportunities.filter(status='completed').count()
            total_positions = sum(o.positions for o in opportunities)
            filled_positions = sum(o.positions_filled for o in opportunities)
            
            opportunity_stats = {
                'total': opportunities.count(),
                'active': active_opportunities,
                'filled': filled_opportunities,
                'completed': completed_opportunities,
                'total_positions': total_positions,
                'filled_positions': filled_positions,
            }
            
            # Get application stats for all opportunities
            all_applications = Application.objects.filter(opportunity__organization=organization_profile)
            pending_applications = all_applications.filter(status='pending').count()
            accepted_applications = all_applications.filter(status='accepted').count()
            
            application_stats = {
                'total': all_applications.count(),
                'pending': pending_applications,
                'accepted': accepted_applications,
            }
            
            context = {
                'organization_profile': organization_profile,
                'opportunities': opportunities[:5],
                'recent_applications': recent_applications,
                'opportunity_stats': opportunity_stats,
                'application_stats': application_stats,
            }
            return render(request, 'accounts/organization_dashboard.html', context)
        
        except OrganizationProfile.DoesNotExist:
            # Organization profile not complete
            messages.warning(request, 'Please complete your organization profile to access dashboard features.')
            return redirect('edit_organization_profile')
    
    else:
        # Unknown user type
        messages.error(request, 'Invalid user type. Please contact an administrator.')
        return redirect('home')