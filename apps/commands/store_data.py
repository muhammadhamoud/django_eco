import os
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()


from django.core.management import call_command
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from store.models import Category, Product, ProductLabel, ProductImage, Currency, ProductPrice, ProductViews, ProductFile

# Initialize the Faker instance
fake = Faker()

# Create a function to generate fake data for each model
def generate_fake_data():
    # Create categories
    categories = []
    for _ in range(5):
        category = Category.objects.create(name=fake.word())
        categories.append(category)

    # Create product labels
    labels = []
    for _ in range(5):
        label = ProductLabel.objects.create(name=fake.word())
        labels.append(label)

    # Create currencies
    currencies = []
    for _ in range(3):
        currency = Currency.objects.create(
            code=fake.unique.random_int(min=100, max=999),
            name=fake.currency_name(),
            symbol=fake.currency_code(),
        )
        currencies.append(currency)

    # Create products with related data
    for _ in range(10):
        product = Product.objects.create(
            name=fake.catch_phrase(),
            category=random.choice(categories),
            label=random.choice(labels),
            stock=random.randint(1, 100),
            views=random.randint(1, 1000),
            purchases=random.randint(1, 1000),
        )

        # Create product images
        for _ in range(3):
            ProductImage.objects.create(
                name=product,
                image=fake.image_url(width=800, height=600),
            )

        # Create product prices
        for _ in range(3):
            price = ProductPrice.objects.create(
                product=product,
                currency=random.choice(currencies),
                price=fake.pydecimal(min_value=10, max_value=1000, right_digits=2),
                start_date=timezone.now(),
                end_date=timezone.now() + timezone.timedelta(days=30),
                period=random.choice(['D', 'W', 'M']),
            )

        # Create product views
        for _ in range(5):
            ProductViews.objects.create(
                ip_address=fake.ipv4(),
                product=product,
            )

        # # Create product files
        # for _ in range(2):
        #     ProductFile.objects.create(
        #         product=product,
        #         file=fake.file_name(category='downloads'),
        #     )

if __name__ == "__main__":
    generate_fake_data()
    print("Fake data generation completed.")
