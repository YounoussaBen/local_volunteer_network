# core/management/commands/setup_project.py

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Sets up the project with initial data and creates a superuser if needed'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset the database before loading fixtures',
        )
    
    def handle(self, *args, **options):
        # Check if reset is requested
        if options['reset']:
            self.stdout.write(self.style.WARNING('Resetting database...'))
            
            # Remove existing database
            db_path = settings.DATABASES['default']['NAME']
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS('Database removed.'))
            
            # Run migrations
            self.stdout.write(self.style.WARNING('Running migrations...'))
            call_command('migrate')
        
        # Create fixtures directory if it doesn't exist
        fixtures_dir = os.path.join(settings.BASE_DIR, 'fixtures')
        if not os.path.exists(fixtures_dir):
            os.makedirs(fixtures_dir)
            self.stdout.write(self.style.SUCCESS('Created fixtures directory.'))
        
        # Load fixtures
        self.stdout.write(self.style.WARNING('Loading initial data...'))
        fixtures_path = os.path.join(fixtures_dir, 'initial_data.json')
        
        if os.path.exists(fixtures_path):
            try:
                call_command('loaddata', fixtures_path)
                self.stdout.write(self.style.SUCCESS('✅ Initial data loaded successfully.'))
                
                # Count imported records
                from django.apps import apps
                from accounts.models import Skill, Interest, UserProfile, VolunteerProfile, OrganizationProfile
                from opportunities.models import Opportunity, Application
                from core.models import FAQ
                
                skill_count = Skill.objects.count()
                interest_count = Interest.objects.count()
                user_count = User.objects.count()
                volunteer_count = VolunteerProfile.objects.count()
                org_count = OrganizationProfile.objects.count()
                opportunity_count = Opportunity.objects.count()
                application_count = Application.objects.count()
                faq_count = FAQ.objects.count()
                
                self.stdout.write(self.style.SUCCESS(f'''
Data imported:
  • {user_count} Users
  • {volunteer_count} Volunteers
  • {org_count} Organizations
  • {skill_count} Skills
  • {interest_count} Interests
  • {opportunity_count} Opportunities
  • {application_count} Applications
  • {faq_count} FAQs
                '''))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load fixtures: {str(e)}'))
        else:
            self.stdout.write(self.style.ERROR(f'⚠️ Fixture file not found at {fixtures_path}'))
            self.stdout.write(self.style.WARNING('Please create the initial_data.json file in the fixtures directory.'))
        
        # Check if superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('No superuser found. Creating one...'))
            
            # Create a default superuser (for development only)
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            
            self.stdout.write(self.style.SUCCESS('Superuser created with username "admin" and password "adminpassword"'))
            self.stdout.write(self.style.WARNING('IMPORTANT: Change this password in production!'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists.'))
        
        # Print login credentials for test users
        self.stdout.write(self.style.SUCCESS('''
🔑 Login Credentials for Test Users:
  • Volunteer: kofi_mensah / adminpassword
  • Volunteer: adwoa_boateng / adminpassword  
  • Volunteer: kwame_asante / adminpassword
  • Organization: hope_foundation / adminpassword
  • Organization: green_ghana / adminpassword
  • Organization: accra_arts_collective / adminpassword
  • Admin: admin / adminpassword
        '''))
        
        self.stdout.write(self.style.SUCCESS('🎉 Project setup complete! Run the server with "python manage.py runserver"'))