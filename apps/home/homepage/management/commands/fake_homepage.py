from django.core.management.base import BaseCommand
from faker import Faker
from homepage.models import SiteInformation, Marketing, Service, Feature, BusinessCategory, Offering, Project, TeamMember, Testimonial

fake = Faker()

# List of Bootstrap icon names
import random
bootstrap_icons = [
    'bi-alarm', 'bi-award', 'bi-bell', 'bi-bookmark', 'bi-calendar', 'bi-chat',  # Add more icons as needed
]
image_urls = [
    'no-image.jpg'
]

class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--num-instances', type=int, default=5, help='Number of fake data instances to generate')

    def handle(self, *args, **options):

        flush_models = [
            SiteInformation, Marketing, Service, Feature,
            BusinessCategory, Offering, Project, TeamMember, Testimonial
        ]

        if options['flush']:
            # Flush (truncate) the tables for specified models
            for model in flush_models:
                model._default_manager.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully flushed {model._meta.verbose_name_plural} table.'))

        if options['generate']:
            # Check if there are existing SiteInformation instances
            existing_sites = SiteInformation.objects.all().first()
            # print(existing_sites)

            if existing_sites is None:
                site_info = SiteInformation(
                    site_name=fake.company(),
                    company_name=fake.company(),
                    site_description=fake.text(),
                    site_keywords=' '.join(fake.words(nb=5)),  # Generate a space-separated list of words
                    tagline=fake.sentence(),
                    address=fake.address(),
                    telephone=fake.phone_number(),
                    mobile=fake.phone_number(),
                    fax=fake.phone_number(),
                    email=fake.email(),
                    website=fake.url(),
                    sales_email=fake.email(),
                    technical_email=fake.email(),
                    accounts_email=fake.email(),
                    facebook_url=fake.url(),
                    twitter_url=fake.url(),
                    instagram_url=fake.url(),
                    linkedin_url=fake.url(),
                    whatsapp_url=fake.url(),
                    googlemap_url=fake.url(),
                    about_us=fake.paragraph(),
                    privacy_policy=fake.paragraph(),
                    terms_of_service=fake.paragraph(),
                    # Add more fields
                )
                site_info.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created SiteInformation: {site_info.site_name}'))
            else:
                site_info = existing_sites
                self.stdout.write(self.style.SUCCESS('SiteInformation instance already exists. No additional sites were generated.'))

            Offering_category = BusinessCategory(
                site=site_info,
                name=fake.word(),
                description=fake.text(),
            )
            Offering_category.save()

            def get_random_category():
                # Get a list of existing BusinessCategory objects
                categories = BusinessCategory.objects.all()
                if categories:
                    # Randomly select a category from the list
                    return random.choice(categories)
                else:
                    # If no categories exist, return None
                    return None

            def generate_fake_data(model_class, num_instances):
                for _ in range(num_instances):
                    fake_data = {
                        "site": site_info,
                        'name': fake.company(),
                        'description': fake.text(),
                        'image': random.choice(image_urls),
                        'icon': random.choice(bootstrap_icons),
                    }

                    if model_class == Testimonial:
                        fake_data.update({
                            'job_title': fake.job(),
                            'company': fake.company(),
                            'content': fake.paragraph(),
                        })

                    elif model_class == Offering:  # Check for the Offering model
                        Offering_category = get_random_category() # Get a random category
                        fake_data.update({
                            'category': Offering_category,
                        })
                    
                    elif model_class == Project:
                        Offering_category = get_random_category()
                        fake_data.update({
                            'category': Offering_category,
                            'client': fake.company(),
                            'file': "path/to/your/file.pdf",
                            'is_published': fake.boolean(),
                        })
                    
                    elif model_class == TeamMember:
                        fake_data.update({
                        'job_title': fake.job(),
                        'email': fake.email(),
                        'phone_number': fake.phone_number(),
                        'bio': fake.text()
                    })

                    instance = model_class(**fake_data)
                    instance.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully created {model_class.__name__}: {instance.name}'))

            for model_class in [Marketing, Service, Feature, Offering, Project, TeamMember, Testimonial]:
                # Example usage for generating Testimonial instances
                generate_fake_data(model_class, 5)
