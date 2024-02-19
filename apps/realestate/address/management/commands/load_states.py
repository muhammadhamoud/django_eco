# yourappname/management/commands/load_states.py

import json
from django.core.management.base import BaseCommand
from address.models import State, Country

states_data = [
    {"country": "US", "name": 'Alabama', "abbreviation": 'AL'},
    {"country": "US", "name": 'Alaska', "abbreviation": 'AK'},
    {"country": "US", "name": 'American Samoa', "abbreviation": 'AS'},
    {"country": "US", "name": 'Arizona', "abbreviation": 'AZ'},
    {"country": "US", "name": 'Arkansas', "abbreviation": 'AR'},
    {"country": "US", "name": 'California', "abbreviation": 'CA'},
    {"country": "US", "name": 'Colorado', "abbreviation": 'CO'},
    {"country": "US", "name": 'Connecticut', "abbreviation": 'CT'},
    {"country": "US", "name": 'Delaware', "abbreviation": 'DE'},
    {"country": "US", "name": 'District Of Columbia', "abbreviation": 'DC'},
    {"country": "US", "name": 'Federated States Of Micronesia', "abbreviation": 'FM'},
    {"country": "US", "name": 'Florida', "abbreviation": 'FL'},
    {"country": "US", "name": 'Georgia', "abbreviation": 'GA'},
    {"country": "US", "name": 'Guam', "abbreviation": 'GU'},
    {"country": "US", "name": 'Hawaii', "abbreviation": 'HI'},
    {"country": "US", "name": 'Idaho', "abbreviation": 'ID'},
    {"country": "US", "name": 'Illinois', "abbreviation": 'IL'},
    {"country": "US", "name": 'Indiana', "abbreviation": 'IN'},
    {"country": "US", "name": 'Iowa', "abbreviation": 'IA'},
    {"country": "US", "name": 'Kansas', "abbreviation": 'KS'},
    {"country": "US", "name": 'Kentucky', "abbreviation": 'KY'},
    {"country": "US", "name": 'Louisiana', "abbreviation": 'LA'},
    {"country": "US", "name": 'Maine', "abbreviation": 'ME'},
    {"country": "US", "name": 'Marshall Islands', "abbreviation": 'MH'},
    {"country": "US", "name": 'Maryland', "abbreviation": 'MD'},
    {"country": "US", "name": 'Massachusetts', "abbreviation": 'MA'},
    {"country": "US", "name": 'Michigan', "abbreviation": 'MI'},
    {"country": "US", "name": 'Minnesota', "abbreviation": 'MN'},
    {"country": "US", "name": 'Mississippi', "abbreviation": 'MS'},
    {"country": "US", "name": 'Missouri', "abbreviation": 'MO'},
    {"country": "US", "name": 'Montana', "abbreviation": 'MT'},
    {"country": "US", "name": 'Nebraska', "abbreviation": 'NE'},
    {"country": "US", "name": 'Nevada', "abbreviation": 'NV'},
    {"country": "US", "name": 'New Hampshire', "abbreviation": 'NH'},
    {"country": "US", "name": 'New Jersey', "abbreviation": 'NJ'},
    {"country": "US", "name": 'New Mexico', "abbreviation": 'NM'},
    {"country": "US", "name": 'New York', "abbreviation": 'NY'},
    {"country": "US", "name": 'North Carolina', "abbreviation": 'NC'},
    {"country": "US", "name": 'North Dakota', "abbreviation": 'ND'},
    {"country": "US", "name": 'Northern Mariana Islands', "abbreviation": 'MP'},
    {"country": "US", "name": 'Ohio', "abbreviation": 'OH'},
    {"country": "US", "name": 'Oklahoma', "abbreviation": 'OK'},
    {"country": "US", "name": 'Oregon', "abbreviation": 'OR'},
    {"country": "US", "name": 'Palau', "abbreviation": 'PW'},
    {"country": "US", "name": 'Pennsylvania', "abbreviation": 'PA'},
    {"country": "US", "name": 'Puerto Rico', "abbreviation": 'PR'},
    {"country": "US", "name": 'Rhode Island', "abbreviation": 'RI'},
    {"country": "US", "name": 'South Carolina', "abbreviation": 'SC'},
    {"country": "US", "name": 'South Dakota', "abbreviation": 'SD'},
    {"country": "US", "name": 'Tennessee', "abbreviation": 'TN'},
    {"country": "US", "name": 'Texas', "abbreviation": 'TX'},
    {"country": "US", "name": 'Utah', "abbreviation": 'UT'},
    {"country": "US", "name": 'Vermont', "abbreviation": 'VT'},
    {"country": "US", "name": 'Virgin Islands', "abbreviation": 'VI'},
    {"country": "US", "name": 'Virginia', "abbreviation": 'VA'},
    {"country": "US", "name": 'Washington', "abbreviation": 'WA'},
    {"country": "US", "name": 'West Virginia', "abbreviation": 'WV'},
    {"country": "US", "name": 'Wisconsin', "abbreviation": 'WI'},
    {"country": "US", "name": 'Wyoming', "abbreviation": 'WY'}
]

class Command(BaseCommand):
    help = 'Load states data into the State model'

    def handle(self, *args, **options):
        for state_data in states_data:
            country_code = state_data.pop('country')
            
            country = Country.objects.get(country=country_code)
            
            State.objects.create(country=country, **state_data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded states data'))