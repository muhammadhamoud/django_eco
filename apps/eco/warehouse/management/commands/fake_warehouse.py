from django.core.management.base import BaseCommand
from faker import Faker
from warehouse.models import *

from django.apps import apps

def flush_models_in_apps(apps_to_flush):
    print(apps_to_flush)
    for app_name in apps_to_flush:
        for model in apps.get_app_config(app_name).get_models():
            model._default_manager.all().delete()
            print(f'Successfully flushed data from all models in app {app_name}.')


fake = Faker()

# List of Bootstrap icon names
import random
bootstrap_icons = [
    'bi-alarm', 'bi-award', 'bi-bell', 'bi-bookmark', 'bi-calendar', 'bi-chat',  # Add more icons as needed
]
image_urls = [
    'no-image.jpg'
]

# python manage.py fake_warehouse --apps-to-flash

# python manage.py fake_warehouse --generate --num-instances=10 category attribute tag productlabel product


def generate_fake_category(num_instances=5):
    for _ in range(num_instances):
        category = Category()
        category.name = fake.word()
        category.save()

def generate_fake_data(model_class, num_instances=5, **kwargs):
    for _ in range(num_instances):
        instance = model_class(**kwargs)
        instance.name = fake.word()
        instance.description = fake.text()
        instance.save()

def create_fake_currencies():
    try:
        currencies = []
        currency_data = [
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "JOR", "name": "Jordanian Dinar", "symbol": "دينار"},
            # Add more currencies as needed
        ]
        for data in currency_data:
            currency = Currency.objects.create(**data)
            currencies.append(currency)
    except:
        pass
    return currencies

def generate_fake_coupons(num_instances=5):
    used_coupon_codes = set()  # Keep track of used coupon codes
    for _ in range(num_instances):
        coupon = Coupon()
        coupon.code = generate_unique_coupon_code(used_coupon_codes)
        coupon.discount_amount = fake.pydecimal(left_digits=2, right_digits=4, min_value=0, max_value=1)
        coupon.start_date = fake.date_between(start_date='-30d', end_date='today')
        coupon.end_date = fake.date_between_dates(date_start=coupon.start_date, date_end=timezone.now().date() + timezone.timedelta(days=30))
        try:
            coupon.save()
            used_coupon_codes.add(coupon.code)
        except:
            pass

def generate_fake_products(num_instances=30, category=None, label=None):
    for _ in range(num_instances):
        product = Product()
        product.category = category  # Assign a valid Category instance
        product.label = label  # Assign a valid ProductLabel instance
        product.name = fake.word()
        product.description = fake.text()
        product.stock = fake.random_int(min=1, max=1000)
        product.views = fake.random_int(min=0, max=1)
        product.average_rating = fake.random_int(min=0, max=5)
        product.purchases = fake.random_int(min=0, max=1000)
        product.is_active = fake.boolean(chance_of_getting_true=80)
        product.is_deleted = fake.boolean(chance_of_getting_true=5)
        product.is_digital = fake.boolean(chance_of_getting_true=50)
        product.is_featured = fake.boolean(chance_of_getting_true=30)
        product.is_new_arrival = fake.boolean(chance_of_getting_true=20)
        product.save()

def generate_unique_coupon_code(used_coupon_codes):
    # while True:
    coupon_code = fake.random_element(['SAVE10', 'DISCOUNT20', 'GET50OFF', 'FREESHIP', 'HAMOUD', 'MUHAMMAD'])
    if coupon_code not in used_coupon_codes:
        return coupon_code


class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--apps-to-flush', nargs='+', type=str, default=[], help='Specify apps to flush (default: current app)')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--num-instances', type=int, default=5, help='Number of fake data instances to generate')

    def flush_models_in_apps(self, apps_to_flush):
        for app_name in apps_to_flush:
            for model in apps.get_app_config(app_name).get_models():
                model._default_manager.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully flushed data from all models in app {app_name}.'))


    def handle(self, *args, **options):
        if options['flush']:
            apps_to_flush = options['apps_to_flush']
            if not apps_to_flush:
                current_app = self.get_app_name()
                if current_app:
                    apps_to_flush = [current_app]

            if apps_to_flush:
                self.flush_models_in_apps(apps_to_flush)
            else:
                self.stdout.write(self.style.WARNING('No apps specified to flush.'))
        
        if options['generate']:
            num_instances = options['num_instances']
            create_fake_currencies()
            generate_fake_category(num_instances)
            generate_fake_coupons(num_instances)
            generate_fake_data(Attribute, num_instances)
            generate_fake_data(Tag, num_instances)
            generate_fake_data(ProductLabel, num_instances)


            # Generate fake data for models
            categories = Category.objects.all()
            labels = ProductLabel.objects.all()
            # print(labels)
            generate_fake_products(num_instances, category=random.choice(categories), label=random.choice(labels))

            print(num_instances)

            app_name = 'Category'
            self.stdout.write(self.style.SUCCESS(f'Successfully generated data for {app_name}.'))
            
            # generate_fake_attribute(num_instances)
            # generate_fake_tag(num_instances)
            # generate_fake_productlabel(num_instances)
            # generate_fake_product(num_instances)

               
            # if 'attribute' in options:
            # if 'tag' in options:
            # if 'productlabel' in options:
            # if 'product' in options:

    def get_app_name(self):
        # Custom method to get the current app name based on your project structure.
        # You might need to modify this to fit your project's structure.
        return "warehouse"  # Replace with the actual app name

