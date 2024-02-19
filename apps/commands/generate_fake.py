import os
import random
from faker import Faker
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()

from homepage.models import (
    Marketing, Service, Feature, Category, Post, ProductCategory,
    Product, Project, TeamMember, Testimonial,
)

fake = Faker()

def create_fake_marketing_data():
    for _ in range(10):  # Create 10 fake Marketing records
        marketing = Marketing(
            name=fake.company(),
            description=fake.paragraph(),
            image='home/marketing/' + fake.file_name(extension='jpg'),
            action=fake.word(),
            action_url=fake.url()
        )
        marketing.save()

def create_fake_service_data():
    for _ in range(10):  # Create 10 fake Service records
        service = Service(
            name=fake.company(),
            discriptions=fake.paragraph(),
            image='home/service/' + fake.file_name(extension='jpg'),
            icon=fake.word()
        )
        service.save()

def create_fake_feature_data():
    for _ in range(10):  # Create 10 fake Feature records
        feature = Feature(
            name=fake.company(),
            discriptions=fake.paragraph(),
            image='home/feature/' + fake.file_name(extension='jpg'),
            icon=fake.word()
        )
        feature.save()

def create_fake_category_data():
    for _ in range(10):  # Create 10 fake Category records
        category = Category(
            name=fake.word(),
            slug=fake.slug()
        )
        category.save()

def create_fake_post_data():
    for _ in range(10):  # Create 10 fake Post records
        post = Post(
            title=fake.sentence(),
            slug=fake.slug(),
            author_id=random.randint(1, 10),  # Replace with appropriate user IDs
            content=fake.paragraph(),
        )
        post.save()
        # Add categories to the post (choose random categories)
        categories = Category.objects.all()
        random_categories = random.sample(list(categories), random.randint(1, 3))
        post.categories.set(random_categories)
        post.save()

def create_fake_product_category_data():
    for _ in range(10):  # Create 10 fake ProductCategory records
        product_category = ProductCategory(
            name=fake.word(),
            description_short=fake.sentence(),
            description=fake.paragraph(),
            image='home/product/' + fake.file_name(extension='jpg'),
        )
        product_category.save()

def create_fake_product_data():
    product_categories = ProductCategory.objects.all()
    for _ in range(20):  # Create 20 fake Product records
        product = Product(
            name=fake.word(),
            description=fake.paragraph(),
            category=random.choice(product_categories),
        )
        product.save()

def create_fake_project_data():
    product_categories = ProductCategory.objects.all()
    for _ in range(10):  # Create 10 fake Project records
        project = Project(
            category=random.choice(product_categories),
            name=fake.sentence(),
            client=fake.company(),
            discriptions=fake.paragraph(),
            file='some_file.pdf',  # Replace with an actual file path
            image='home/project/' + fake.file_name(extension='jpg'),
            icon=fake.word(),
            is_published=fake.boolean(),
        )
        project.save()

def create_fake_teammember_data():
    for _ in range(10):  # Create 10 fake TeamMember records
        team_member = TeamMember(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            job_title=fake.job(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            bio=fake.paragraph(),
            linkedin_url=fake.url(),
            twitter_url=fake.url(),
            facebook_url=fake.url(),
            instagram_url=fake.url(),
            profile_image='home/team/' + fake.file_name(extension='jpg'),
        )
        team_member.save()

def create_fake_testimonial_data():
    for _ in range(10):  # Create 10 fake Testimonial records
        testimonial = Testimonial(
            name=fake.name(),
            company=fake.company(),
            content=fake.paragraph(),
        )
        testimonial.save()

if __name__ == '__main__':
    create_fake_marketing_data()
    create_fake_service_data()
    create_fake_feature_data()
    create_fake_category_data()
    # create_fake_post_data()
    create_fake_product_category_data()
    create_fake_product_data()
    create_fake_project_data()
    create_fake_teammember_data()
    create_fake_testimonial_data()
    print("Fake data creation completed.")