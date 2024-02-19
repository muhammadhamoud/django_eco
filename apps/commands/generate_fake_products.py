import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from faker import Faker
from products.models import Category, Product

from django.contrib.auth import get_user_model
User = get_user_model()

fake = Faker()

def generate_fake_data():
    for _ in range(2):  # Generate 10 fake categories
        category = Category.objects.create(
            name=fake.word(),
            icon=fake.image_url(),
        )
        for _ in range(5):  # Generate 5 fake products for each category
            seller = User.objects.first()
            Product.objects.create(
                seller=seller,  # Replace with a user instance if needed
                category=category,
                title=fake.catch_phrase(),
                price = fake.random_number(digits=2, fix_len=True),
                image= "https://picsum.photos/200", #fake.image_url(),
                description=fake.paragraph(),
                quantity=fake.random_int(min=1, max=100),
                views=fake.random_int(min=0, max=1),
            )

if __name__ == "__main__":
    generate_fake_data()
