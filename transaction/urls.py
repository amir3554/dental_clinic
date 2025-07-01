from django.urls import path
from .views import (get_publishable_key, stripe_transaction, check_out_complete,
stripe_webhook , check_out, paypal_transaction)
from paypal.standard.ipn.views import ipn

urlpatterns = [
    path('stripe/config/publishable-key/', get_publishable_key, name='GetPublishableKey'),
    path('stripe/<int:appointment_id>', stripe_transaction, name="StripeTransaction"),
    path('stripe/webhook/', stripe_webhook, name='StripeWebhook'),
    path('check-out/<int:appointment_id>/', check_out, name='CheckOut'),
    path('check-out-complete/', check_out_complete, name='CheckOutComplete'),
    path('paypal/<int:appointment_id>/', paypal_transaction, name='CheckoutPaypal'),
    path('paypal/webhook/', ipn, name='CheckoutPaypalWebhook'),
]
