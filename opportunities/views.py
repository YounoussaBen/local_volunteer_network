# opportunities/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseForbidden

from .models import Opportunity, Application
from .forms import (
    OpportunityForm, ApplicationForm, ApplicationStatusForm,
    VolunteerFeedbackForm, OrganizationFeedbackForm
)
from accounts.models import Skill, Interest

def opportunity_list(request):
    """View list of all active opportunities with filtering options"""
    opportunities = Opportunity.objects.filter(status='active').order_by('-created_at')
    
    # Get filter parameters
    query = request.GET.get('q')
    location = request.GET.get('location')
    skill_ids = request.GET.getlist('skills')
    interest_ids = request.GET.getlist('interests')
    
    # Apply filters if provided
    if query:
        opportunities = opportunities.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    
    if location:
        opportunities = opportunities.filter(location__icontains=location)
    
    if skill_ids:
        opportunities = opportunities.filter(required_skills__id__in=skill_ids).distinct()
    
    if interest_ids:
        opportunities = opportunities.filter(interests__id__in=interest_ids).distinct()
    
    # Get all skills and interests for filter dropdowns
    skills = Skill.objects.all()
    interests = Interest.objects.all()
    
    context = {
        'opportunities': opportunities,
        'skills': skills,
        'interests': interests,
        'query': query,
        'location': location,
        'selected_skill_ids': [int(id) for id in skill_ids] if skill_ids else [],
        'selected_interest_ids': [int(id) for id in interest_ids] if interest_ids else []
    }
    
    return render(request, 'opportunities/opportunity_list.html', context)

def opportunity_detail(request, pk):
    """View detailed information about an opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    # Check if the current user has already applied for this opportunity
    has_applied = False
    application = None
    
    if request.user.is_authenticated:
        try:
            volunteer_profile = request.user.profile.volunteer_profile
            application = Application.objects.filter(
                opportunity=opportunity,
                volunteer=volunteer_profile
            ).first()
            has_applied = application is not None
        except:
            pass
    
    context = {
        'opportunity': opportunity,
        'has_applied': has_applied,
        'application': application
    }
    
    return render(request, 'opportunities/opportunity_detail.html', context)

@login_required
def create_opportunity(request):
    """Create a new volunteer opportunity"""
    user_profile = request.user.profile
    
    # Check if user is an organization
    if user_profile.user_type != 'organization':
        messages.error(request, 'Only organizations can create volunteer opportunities.')
        return redirect('opportunity_list')
    
    try:
        organization_profile = user_profile.organization_profile
    except:
        messages.error(request, 'Please complete your organization profile first.')
        return redirect('edit_organization_profile')
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.organization = organization_profile
            opportunity.save()
            
            # Save many-to-many fields
            form.save_m2m()
            
            messages.success(request, 'Volunteer opportunity created successfully!')
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()
    
    return render(request, 'opportunities/create_opportunity.html', {'form': form})

@login_required
def edit_opportunity(request, pk):
    """Edit an existing volunteer opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    # Check if the user is the owner of this opportunity
    if request.user.profile.user_type != 'organization' or opportunity.organization != request.user.profile.organization_profile:
        return HttpResponseForbidden("You don't have permission to edit this opportunity.")
    
    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated successfully!')
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)
    
    return render(request, 'opportunities/edit_opportunity.html', {'form': form, 'opportunity': opportunity})

@login_required
def delete_opportunity(request, pk):
    """Delete a volunteer opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=pk)
    
    # Check if the user is the owner of this opportunity
    if request.user.profile.user_type != 'organization' or opportunity.organization != request.user.profile.organization_profile:
        return HttpResponseForbidden("You don't have permission to delete this opportunity.")
    
    if request.method == 'POST':
        opportunity.delete()
        messages.success(request, 'Opportunity deleted successfully!')
        return redirect('opportunity_list')
    
    return render(request, 'opportunities/delete_opportunity.html', {'opportunity': opportunity})

@login_required
def apply_opportunity(request, pk):
    """Apply for a volunteer opportunity"""
    opportunity = get_object_or_404(Opportunity, pk=pk)
    user_profile = request.user.profile
    
    # Check if user is a volunteer
    if user_profile.user_type != 'volunteer':
        messages.error(request, 'Only volunteers can apply for opportunities.')
        return redirect('opportunity_detail', pk=pk)
    
    volunteer_profile = user_profile.volunteer_profile
    
    # Check if already applied
    existing_application = Application.objects.filter(
        opportunity=opportunity,
        volunteer=volunteer_profile
    ).exists()
    
    if existing_application:
        messages.info(request, 'You have already applied for this opportunity.')
        return redirect('opportunity_detail', pk=pk)
    
    # Check if opportunity is still active and not full
    if opportunity.status != 'active':
        messages.error(request, 'This opportunity is no longer accepting applications.')
        return redirect('opportunity_detail', pk=pk)
    
    if opportunity.is_full:
        messages.error(request, 'This opportunity has filled all available positions.')
        return redirect('opportunity_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.opportunity = opportunity
            application.volunteer = volunteer_profile
            application.save()
            
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('application_list')
    else:
        form = ApplicationForm()
    
    return render(request, 'opportunities/apply_opportunity.html', {
        'form': form,
        'opportunity': opportunity
    })

@login_required
def application_list(request):
    """View list of all applications for the current user"""
    user_profile = request.user.profile

    if user_profile.user_type == 'volunteer':
        try:
            volunteer_profile = user_profile.volunteer_profile
            applications = volunteer_profile.applications.all().order_by('-created_at')
            return render(request, 'opportunities/volunteer_application_list.html', {'applications': applications})
        except:
            messages.error(request, 'Please complete your volunteer profile first.')
            return redirect('edit_volunteer_profile')

    elif user_profile.user_type == 'organization':
        if not hasattr(user_profile, 'organization_profile'):
            messages.error(request, 'Please complete your organization profile first.')
            return redirect('edit_organization_profile')

        organization_profile = user_profile.organization_profile

        if not organization_profile.organization_name:
            messages.error(request, 'Please complete your organization profile with all required fields.')
            return redirect('edit_organization_profile')

        opportunities = organization_profile.opportunities.all()
        applications = Application.objects.filter(opportunity__in=opportunities).order_by('-created_at')

        # Count by status
        pending_count = applications.filter(status="pending").count()
        accepted_count = applications.filter(status="accepted").count()
        declined_count = applications.filter(status="declined").count()

        context = {
            'applications': applications,
            'pending_count': pending_count,
            'accepted_count': accepted_count,
            'declined_count': declined_count,
        }
        return render(request, 'opportunities/organization_application_list.html', context)

    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')

@login_required
def application_detail(request, pk):
    """View detailed information about an application"""
    application = get_object_or_404(Application, pk=pk)
    user_profile = request.user.profile
    
    # Check if the user has permission to view this application
    if user_profile.user_type == 'volunteer':
        try:
            if application.volunteer != user_profile.volunteer_profile:
                return HttpResponseForbidden("You don't have permission to view this application.")
        except:
            return HttpResponseForbidden("Profile not complete.")
    
    elif user_profile.user_type == 'organization':
        try:
            if application.opportunity.organization != user_profile.organization_profile:
                return HttpResponseForbidden("You don't have permission to view this application.")
        except:
            return HttpResponseForbidden("Profile not complete.")
    
    else:
        return HttpResponseForbidden("Invalid user type.")
    
    return render(request, 'opportunities/application_detail.html', {'application': application})

@login_required
def update_application(request, pk):
    """Update the status of an application (for organizations)"""
    application = get_object_or_404(Application, pk=pk)
    user_profile = request.user.profile
    
    # Check if the user is the organization owner of this opportunity
    if user_profile.user_type != 'organization' or application.opportunity.organization != user_profile.organization_profile:
        return HttpResponseForbidden("You don't have permission to update this application.")
    
    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            
            # Update opportunity status if all positions are filled
            application.opportunity.update_status()
            
            messages.success(request, 'Application status updated successfully!')
            return redirect('application_detail', pk=application.pk)
    else:
        form = ApplicationStatusForm(instance=application)
    
    return render(request, 'opportunities/update_application.html', {'form': form, 'application': application})

@login_required
def add_feedback(request, pk):
    """Add feedback after a volunteer opportunity (for both volunteers and organizations)"""
    application = get_object_or_404(Application, pk=pk)
    user_profile = request.user.profile
    
    # Check if the opportunity is completed
    if application.opportunity.status != 'completed':
        messages.error(request, 'Feedback can only be provided after the opportunity is completed.')
        return redirect('application_detail', pk=pk)
    
    if user_profile.user_type == 'volunteer':
        # Volunteer providing feedback
        try:
            if application.volunteer != user_profile.volunteer_profile:
                return HttpResponseForbidden("You don't have permission to provide feedback for this application.")
        except:
            return HttpResponseForbidden("Profile not complete.")
        
        if request.method == 'POST':
            form = VolunteerFeedbackForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('application_detail', pk=application.pk)
        else:
            form = VolunteerFeedbackForm(instance=application)
        
        template = 'opportunities/volunteer_feedback.html'
    
    elif user_profile.user_type == 'organization':
        # Organization providing feedback
        try:
            if application.opportunity.organization != user_profile.organization_profile:
                return HttpResponseForbidden("You don't have permission to provide feedback for this application.")
        except:
            return HttpResponseForbidden("Profile not complete.")
        
        if request.method == 'POST':
            form = OrganizationFeedbackForm(request.POST, instance=application)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your feedback has been submitted successfully!')
                return redirect('application_detail', pk=application.pk)
        else:
            form = OrganizationFeedbackForm(instance=application)
        
        template = 'opportunities/organization_feedback.html'
    
    else:
        return HttpResponseForbidden("Invalid user type.")
    
    return render(request, template, {'form': form, 'application': application})