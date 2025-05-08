from django.urls import path
from .views import TwilioWebhookView

urlpatterns = [
    path('message/', TwilioWebhookView.as_view(), name='twilio_webhook'),
] 