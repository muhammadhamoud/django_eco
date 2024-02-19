
from pathlib import Path
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from plotter.models import (Application, Make, Trim, Body, Year, Car, Images, Model, PlotterMachine, BodyPart)
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

current_path = Path(__file__).resolve().parent.parent.parent
df = pd.ExcelFile(os.path.join(current_path, "fixtures", "plotter.xlsx"))

for worksheet in df.sheet_names:
    # print(worksheet)
    data = df.parse(sheet_name=worksheet)
    exec('{} = data'.format(worksheet.lower()))


dataframes = [application, make, trim, body, car, model, plottermachine, bodypart]
models = [Application, Make, Trim, Body, Car, Model, PlotterMachine, BodyPart]

dataframes = [bodypart]
models = [BodyPart]


for model_class in models:
    
    # Construct the dataframe variable name from the model class name
    dataframe_variable_name = model_class.__name__.lower()

    # Assuming the dataframe variable is in the global namespace, retrieve it
    data_frame = globals()[dataframe_variable_name]
    # print(data_frame)
    data_frame.fillna('', inplace=True)

# How to call me
# python manage.py plotter --flush 
# python manage.py plotter --generate 

# List of Bootstrap icon names
import random
bootstrap_icons = [
    'bi-alarm', 'bi-award', 'bi-bell', 'bi-bookmark', 'bi-calendar', 'bi-chat',  # Add more icons as needed
]
image_urls = [
    'no-image.jpg'
]

def update_translations(model, name, description, language_code, *args, **kwargs):
    # Ensure you set the language for which you want to update the translations
    model.set_current_language(language_code)

    # Update the translation fields with the provided data
    model.name = name
    model.description = description

    # Save the translation instance
    model.save()

    # Make sure to set the current language back to the original language
    model.set_current_language('en')  # Replace 'en' with your original language code
    model.save()

    print(f'Successfully created: {model.name}')


def load_data_and_translations(model_class):

    # Construct the dataframe variable name from the model class name
    dataframe_variable_name = model_class.__name__.lower()

    # Assuming the dataframe variable is in the global namespace, retrieve it
    data_frame = globals()[dataframe_variable_name]

    if model_class == Model:
        for row in data_frame.itertuples():
            try:
                make_instance = Make.objects.get(translations__name=row.make)
                # The object with the specified name was found
            except ObjectDoesNotExist:
                # Handle the case where the object with the specified name does not exist
                print(f"Make with name '{row.make}' does not exist.")
                make_instance = None
            
            fake_data = {
                'make': make_instance,
                'name': row.name,
                'description': row.description,
            }
            
            try:
                instance = model_class(**fake_data)
                instance.save()

                # Activate the Arabic language
                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
            
            except Exception as Ex:
                # Handle the case where the object with the specified name does not exist
                print(f"{Ex}")

    elif model_class == BodyPart:
        for row in data_frame.itertuples():
            try:
                application_instance = Application.objects.get(translations__name=row.application)
                # The object with the specified name was found
            except ObjectDoesNotExist:
                # Handle the case where the object with the specified name does not exist
                print(f"Make with name '{row.application}' does not exist.")
                application_instance = None
            
            fake_data = {
                'application': application_instance,
                'name': row.name,
                'description': row.description,
            }
            
            try:
                instance = model_class(**fake_data)
                instance.save()

                # Activate the Arabic language
                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
            
            except Exception as Ex:
                # Handle the case where the object with the specified name does not exist
                print(f"{Ex}")


    elif model_class == PlotterMachine:
        for row in data_frame.itertuples():
            fake_data = {
                'name': row.name,
            }
            try:
                instance = model_class(**fake_data)
                instance.save()
            except Exception as Ex:
                print(f"{Ex}")

    else:
        for row in data_frame.itertuples():
            fake_data = {
                'name': row.name,
                'description': row.description,
            }
            try:
                instance = model_class(**fake_data)
                instance.save()
                
                # Activate the Arabic language
                update_translations(
                    model=instance, 
                    name=row.name_ar, 
                    description=row.description_ar, 
                    language_code='ar'
                )
            except Exception as Ex:
                # Handle the case where the object with the specified name does not exist
                print(f"{Ex}")



class Command(BaseCommand):
    help = 'Flush (truncate) or generate fake data for specified models'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Flush (truncate) model tables')
        parser.add_argument('--generate', action='store_true', help='Generate fake data for model tables')
        parser.add_argument('--num-instances', type=int, default=5, help='Number of fake data instances to generate')

    def handle(self, *args, **options):

        flush_models = models

        if options['flush']:
            # Flush (truncate) the tables for specified models
            for model in flush_models:
                model._default_manager.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully flushed {model._meta.verbose_name_plural} table.'))

        if options['generate']:
            for model in models:
                load_data_and_translations(model_class=model)

          

