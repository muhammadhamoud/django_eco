from django.urls import path
from . import views
from . import webhooks

app_name = 'payment'

urlpatterns = [
    path('payment/process/', views.payment_process, name='process'),
    path('payment/completed/', views.payment_completed, name='completed'),
    path('payment/canceled/', views.payment_canceled, name='canceled'),
    path('payment/webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
]
