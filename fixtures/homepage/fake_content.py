import json
import random
from faker import Faker
# from homepage.models import TeamMember

# Initialize the Faker instance
fake = Faker()

# Define a function to generate fake TeamMember data
def generate_fake_teammembers(num_records):
    fake_teammembers = []
    
    # Initialize a variable for the primary key
    next_pk = 1

    for _ in range(num_records):
        # Generate fake data for each field
        first_name = fake.first_name()
        last_name = fake.last_name()
        job_title = fake.job()
        email = fake.email()
        phone_number = fake.phone_number()
        bio = fake.paragraph()

        # Generate optional social media URLs
        if random.choice([True, False]):
            linkedin_url = fake.url()
        else:
            linkedin_url = None

        if random.choice([True, False]):
            twitter_url = fake.url()
        else:
            twitter_url = None

        if random.choice([True, False]):
            facebook_url = fake.url()
        else:
            facebook_url = None

        if random.choice([True, False]):
            instagram_url = fake.url()
        else:
            instagram_url = None

        # Create a dictionary with the fake data
        teammember_data = {
            "model": "homepage.teammember",  # Replace 'myapp' with your app name
            "pk": next_pk,  # Auto-generated primary key
            "fields": {
                "first_name": first_name,
                "last_name": last_name,
                "job_title": job_title,
                "email": email,
                "phone_number": phone_number,
                "bio": bio,
                "linkedin_url": linkedin_url,
                "twitter_url": twitter_url,
                "facebook_url": facebook_url,
                "instagram_url": instagram_url,
            },
        }

        fake_teammembers.append(teammember_data)
        next_pk += 1  # Increment the primary key

    return fake_teammembers

# Generate a specified number of fake TeamMember records
num_records = 10  # Change this to the number of fake records you want to generate
fake_teammembers = generate_fake_teammembers(num_records)

# Save the fake data as a fixture JSON file
fixture_filename = "fake_teammembers_fixture.json"
with open(fixture_filename, "w") as fixture_file:
    json.dump(fake_teammembers, fixture_file, indent=2)

print(f"Fake data saved to {fixture_filename}")
