cd backend\site & python manage.py makemigrations & python manage.py migrate

 python manage.py runserver

python manage.py createsuperuser --username=admin --email=admin@admin.com


python manage.py startapp blog ./apps/home/blog