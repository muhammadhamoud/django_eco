import json

contact_info = {
    "address": "P.O.Box: 21577, Ajman, United Arab Emirates",
    "telephone": "+971-6-7477880",
    "mobile": "+971-50-9169001",
    "fax": "+971-6-7485312",
    "email": "info@aldarwashprefab.com",
    "website": "http://www.aldarwashprefab.com",
    "sales_email": "sales@aldarwashprefab.com",
    "technical_email": "technical@aldarwashprefab.com",
    "accounts_email": "accounts@aldarwashprefab.com"
}

fixture_data = [
    {
        "model": "homepage.contactinformation",  # Replace 'yourappname' with your app's name
        "pk": 1,  # Use a unique primary key
        "fields": contact_info
    }
]

with open('contact_information_fixture.json', 'w') as f:
    json.dump(fixture_data, f, indent=2)
