from django.urls import path
from .views import CustomerInteractionView # Relative import

app_name = 'interaction_api' 

urlpatterns = [
    path('customer_message/', CustomerInteractionView.as_view(), name='customer_message'),
] 