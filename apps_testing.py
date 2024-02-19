import django
import os
os.chdir(fr"C:\Backup\ng\backend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


from pathlib import Path
from django.core.management.base import BaseCommand

from plotter.models import (Application, Make, Trim, Type, Year, Car, Images)
from faker import Faker
fake = Faker()

import pandas as pd
import os
from django.conf import settings

# class Command(BaseCommand):
#     help = 'Flush (truncate) or generate fake data for specified models'
#     def handle(self, *args, **options):
#         current_path = Path(__file__).resolve().parent.parent.parent
#         print(current_path)


current_path = Path(__file__).resolve().parent
file_path = os.path.join(current_path, "apps", "plotters", "plotter" ,"fixtures", "plotter.xlsx")
df = pd.ExcelFile(file_path)

for worksheet in df.sheet_names:
    print(worksheet)
    # exec('{} = worksheet')
    data = df.parse(sheet_name=worksheet)
    exec('{} = data'.format(worksheet.lower()))


dataframes = [type, year, make, model, body, trim, car, application, product, plotter]

for dataframe in dataframes:
    dataframe.fillna('', inplace=True)


current_path = Path(__file__).resolve().parent.parent.parent
df = pd.ExcelFile(os.path.join(current_path, "fixtures", "plotter.xlsx"))

for model in [Application, Make, Trim, Type, Year, Car, Images]:
    print(model)


for row in type.itertuples():
    model_class = Type
    fake_data = {
        'name': row.name,
        'description': row.description,
    }

    instance = model_class(**fake_data)
    instance.save()

    update_translations(
        model=instance, 
        name=row.name_ar, 
        description=row.description_ar, 
        language_code='ar'
    )























from django_countries import countries















from address.models import Country

country = Country.objects.all().first()

countries().name


import pandas as pd
import os
from django.conf import settings
df = pd.ExcelFile(os.path.join(settings.BASE_DIR, "fixtures", "roinsight.xlsx"))
site = df.parse(sheet_name='site')
for row in site.itertuples():
    site_info = SiteInformation(
        name=row.name,
        description=row.description,
        company_name=row.company_name,
        keywords=row.keywords,  # Generate a space-separated list of words
        )
    site_info.save()




# from django.utils.text import slugify
# name="Python is great.hamoud.test"
# filename = "test.test.txt"
# slug = slugify(name)
# name, ext = filename.split('.')
# new_filename = f"{slug}.{ext}"
# name, ext = os.path.splitext(filename)