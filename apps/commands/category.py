import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from faker import Faker
from faker import Faker
import random
import datetime
from django.db import transaction

from warehouse.models import Attribute, CartItem, Category, Coupon, Currency, Product, ProductLabel, Tag, Reservation, ProductViews, ProductReview, ProductPurchaseCount, ProductPrice, ProductImage, ProductFile

from django.conf import settings

User = settings.AUTH_USER_MODEL

fake = Faker()

# def create_fake_users(num_users=10):
#     users = []
#     for _ in range(num_users):
#         user = User.objects.create_user(
#             username=fake.user_name(),
#             email=fake.email(),
#             password="password123"
#         )
#         users.append(user)
#     return users

def create_fake_product_label():
    from django.db.utils import IntegrityError

    try:
        product_label = ProductLabel.objects.create(
            name=fake.word(),  # Generate a random word as the label name
            description=fake.sentence(),  # Generate a random sentence as the label description
        )
        return product_label
    except IntegrityError:
        # Handle IntegrityError if a duplicate record is created
        return create_fake_product_label()


def create_fake_attributes(num_attributes=10):
    attributes = []
    for _ in range(num_attributes):
        attribute = Attribute.objects.create(
            name=fake.word(),
            description=fake.text()
        )
        attributes.append(attribute)
    return attributes

def create_fake_categories(num_categories=10):
    categories = []
    for _ in range(num_categories):
        category = Category.objects.create(
            name=fake.word(),
            # Add other category fields here
        )
        categories.append(category)
    return categories

# Define similar functions to create data for other models

def create_fake_coupons(num_coupons=10):
    coupons = []
    for _ in range(num_coupons):
        coupon = Coupon.objects.create(
            code=fake.unique.word(),
            description=fake.text(),
            discount_amount=random.uniform(0.01, 0.5),  # Random discount between 1% and 50%
            start_date=fake.date_between(start_date='-30d', end_date='now'),
            end_date=fake.date_between(start_date='now', end_date='+30d')
        )
        coupons.append(coupon)
    return coupons

def create_fake_currencies():
    currencies = []
    currency_data = [
        {"code": "USD", "name": "US Dollar", "symbol": "$"},
        {"code": "EUR", "name": "Euro", "symbol": "€"},
        # Add more currencies as needed
    ]
    for data in currency_data:
        currency = Currency.objects.create(**data)
        currencies.append(currency)
    return currencies

def create_fake_products(num_products=10):
    products = []
    categories = Category.objects.all()
    product_labels = ProductLabel.objects.all()
    for _ in range(num_products):
        product = Product.objects.create(
            name=fake.unique.word(),
            description=fake.text(),
            stock=random.randint(1, 1000),  
            views=random.randint(1, 1000), 
            average_rating=random.uniform(1, 5),
            purchases=random.randint(1, 1000), 
            is_active=random.choice([True, False]),
            is_deleted=random.choice([True, False]),
            is_digital=random.choice([True, False]),
            is_featured=random.choice([True, False]),
            is_new_arrival=random.choice([True, False]),
            category=random.choice(categories),
            label=random.choice(product_labels)
        )
        products.append(product)
    return products



if __name__ == "__main__":
    num_users = 10
    num_attributes = 10
    num_categories = 10
    num_coupons = 10
    num_currencies = 2  # Assuming you want to create 2 currencies
    num_products = 10

    with transaction.atomic():
        # users = create_fake_users(num_users)
        # random_product_label = create_fake_product_label()

        # attributes = create_fake_attributes(num_attributes)
        # categories = create_fake_categories(num_categories)
        # coupons = create_fake_coupons(num_coupons)
        # currencies = create_fake_currencies()
        products = create_fake_products(num_products)


        # Create data for other models in a similar manner

