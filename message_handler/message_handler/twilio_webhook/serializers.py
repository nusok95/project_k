from rest_framework import serializers
from .models import TwilioMessage

class TwilioMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TwilioMessage
        fields = '__all__' 
    