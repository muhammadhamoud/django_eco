from django_countries import Countries

for i in dir(Countries):
    if not i.startswith('_'):
        print(i)

for translated_code in list(Countries)[:3]:
    print(translated_code)

