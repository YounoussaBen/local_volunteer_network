# accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction


from .models import VolunteerProfile, OrganizationProfile
from .forms import (
    UserRegistrationForm, UserProfileForm, 
    VolunteerProfileForm, OrganizationProfileForm
)

def register(request):
    """View for user to choose registration type"""
    return render(request, 'accounts/register.html')

def register_volunteer(request):
    """View for volunteer registration"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                # Create the user account
                user = user_form.save()
                
                # Update the user profile
                user.profile.user_type = 'volunteer'
                user.profile.save()
                
                # Create volunteer profile
                volunteer_profile = VolunteerProfile.objects.create(user_profile=user.profile)
                
                # Log the user in
                login(request, user)
                
                messages.success(request, 'Registration successful! Please complete your profile.')
                return redirect('edit_volunteer_profile')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'accounts/register_volunteer.html', {'form': user_form})

def register_organization(request):
    """View for organization registration"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            with transaction.atomic():
                # Create the user account
                user = user_form.save()
                
                # Update the user profile
                user.profile.user_type = 'organization'
                user.profile.save()
                
                # Create organization profile
                organization_profile = OrganizationProfile.objects.create(user_profile=user.profile)
                
                # Log the user in
                login(request, user)
                
                messages.success(request, 'Registration successful! Please complete your organization profile.')
                return redirect('edit_organization_profile')
    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'accounts/register_organization.html', {'form': user_form})

@login_required
def view_profile(request):
    """View user's own profile"""
    user_profile = request.user.profile
    
    context = {
        'user_profile': user_profile
    }
    
    if user_profile.user_type == 'volunteer':
        try:
            volunteer_profile = user_profile.volunteer_profile
            context['volunteer_profile'] = volunteer_profile
            return render(request, 'accounts/volunteer_profile.html', context)
        except VolunteerProfile.DoesNotExist:
            messages.warning(request, 'Please complete your volunteer profile.')
            return redirect('edit_volunteer_profile')
    
    elif user_profile.user_type == 'organization':
        try:
            organization_profile = user_profile.organization_profile
            context['organization_profile'] = organization_profile
            return render(request, 'accounts/organization_profile.html', context)
        except OrganizationProfile.DoesNotExist:
            messages.warning(request, 'Please complete your organization profile.')
            return redirect('edit_organization_profile')
    
    else:
        messages.error(request, 'Invalid user type.')
        return redirect('home')

@login_required
def edit_profile(request):
    """Edit basic user profile"""
    user_profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def edit_volunteer_profile(request):
    """Edit volunteer-specific profile"""
    user_profile = request.user.profile
    
    # Check if user is a volunteer
    if user_profile.user_type != 'volunteer':
        messages.error(request, 'Access denied. You are not registered as a volunteer.')
        return redirect('home')
    
    # Get or create volunteer profile
    volunteer_profile, created = VolunteerProfile.objects.get_or_create(user_profile=user_profile)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        volunteer_form = VolunteerProfileForm(request.POST, instance=volunteer_profile)
        
        if profile_form.is_valid() and volunteer_form.is_valid():
            profile_form.save()
            volunteer_form.save()
            
            messages.success(request, 'Your volunteer profile has been updated successfully.')
            return redirect('view_profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        volunteer_form = VolunteerProfileForm(instance=volunteer_profile)
    
    context = {
        'profile_form': profile_form,
        'volunteer_form': volunteer_form
    }
    
    return render(request, 'accounts/edit_volunteer_profile.html', context)

@login_required
def edit_organization_profile(request):
    """Edit organization-specific profile"""
    user_profile = request.user.profile
    
    # Check if user is an organization
    if user_profile.user_type != 'organization':
        messages.error(request, 'Access denied. You are not registered as an organization.')
        return redirect('home')
    
    # Get or create organization profile
    organization_profile, created = OrganizationProfile.objects.get_or_create(user_profile=user_profile)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        organization_form = OrganizationProfileForm(request.POST, instance=organization_profile)
        
        if profile_form.is_valid() and organization_form.is_valid():
            profile_form.save()
            organization_form.save()
            
            messages.success(request, 'Your organization profile has been updated successfully.')
            return redirect('view_profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        organization_form = OrganizationProfileForm(instance=organization_profile)
    
    context = {
        'profile_form': profile_form,
        'organization_form': organization_form
    }
    
    return render(request, 'accounts/edit_organization_profile.html', context)

def volunteer_list(request):
    """View list of all volunteers"""
    # Only show profiles that have skills or interests defined (completed profiles)
    volunteers = VolunteerProfile.objects.filter(
        skills__isnull=False
    ).distinct().order_by('user_profile__user__first_name')
    
    return render(request, 'accounts/volunteer_list.html', {'volunteers': volunteers})

def volunteer_detail(request, pk):
    """View detailed volunteer profile"""
    volunteer_profile = get_object_or_404(VolunteerProfile, pk=pk)
    
    return render(request, 'accounts/volunteer_detail.html', {'volunteer_profile': volunteer_profile})

def organization_list(request):
    """View list of all organizations"""
    organizations = OrganizationProfile.objects.all().order_by('organization_name')
    
    return render(request, 'accounts/organization_list.html', {'organizations': organizations})

def organization_detail(request, pk):
    """View detailed organization profile"""
    organization_profile = get_object_or_404(OrganizationProfile, pk=pk)
    
    # Get recent opportunities from this organization
    opportunities = organization_profile.opportunities.order_by('-created_at')[:5]
    
    context = {
        'organization_profile': organization_profile,
        'opportunities': opportunities
    }
    
    return render(request, 'accounts/organization_detail.html', context)