from rest_framework import serializers

class CustomerMessageRequestSerializer(serializers.Serializer):
    message_content = serializers.CharField(
        max_length=5000, 
        help_text="The text content of the customer's message.",
        allow_blank=False
    )

    def validate_message_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("message_content cannot be empty or just whitespace.")
        return value 