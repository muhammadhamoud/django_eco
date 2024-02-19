import json
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest  # Import WSGIRequest
import requests
import django
from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import os
import django
from django.http import HttpRequest
from django.core.handlers.wsgi import WSGIRequest
import requests
import json

# Set the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# Define a function to make requests using the HttpRequest object
def make_request(request_method, url, data=None):
    """
    >>>request_method='GET'
    >>>data=None
    >>>url=
    """
    # Create a Django HttpRequest object
    request = HttpRequest()
    request.method = request_method  # 'GET' or 'POST'

    if data is not None:
        if request_method == 'GET':
            request.GET = data
        elif request_method == 'POST':
            request._body = json.dumps(data)

    # Create a WSGIRequest object to use the request in a test client
    wsgi_request = WSGIRequest(request.environ)

    # Use Django's test client to make the request
    response = wsgi_request.get_response(application)


    # Print the response status code
    print(f"Response Status Code: {response.status_code}")

    # Print the response content
    print(f"Response Content: {response.content.decode()}")

    return response

# Usage example
if __name__ == "__main__":
    # Example GET request
    response = make_request(request_method='GET', url='/api/product/')

    # Example POST request with JSON data
    data = {'key': 'value'}
    response = make_request(request_method='POST', url='/your_endpoint/', data=data)



def submit_request(request, url, data=None):
    headers = {
        'Content-Type': 'application/json'
        # 'Authorization': 'Bearer "YOUR_TOKEN_HERE"'
    }
    if request == 'POST':
        response = requests.post(f'http://localhost:8000/api/{url}', json=data, headers=headers)

    if request == 'GET':
        response = requests.get(f'http://localhost:8000/api/{url}', headers=headers)

    print(response.status_code)  # prints the status code of the response
    print(response.json())  # prints the JSON content of the response

    return response


products = submit_request(request='GET', url='product/')
products = request(request_method='GET', url="http://localhost:8000/api/product/816ecd6d-77b7-4731-aa90-6be7ed59576c?start_date='2020-02-15'")

products.query_params.get("start_date")

data = {'email': 'admin@admin.com', 'password': 'admin123@'}
login = submit_request(request='POST', url='login/', data=data)

request_method = 'GET'  # 'GET' or 'POST'
url = '/api/your_endpoint/'  # Replace with the actual URL you want to call

# Create a mock Django request object (you should use a real request object in your Django application)
mock_request = WSGIRequest({
    'REQUEST_METHOD': 'GET',  # Adjust the method as needed
    'PATH_INFO': url,
})

response = request(mock_request, request_method, url, data)
from store.models import Product

Product.objects.all()