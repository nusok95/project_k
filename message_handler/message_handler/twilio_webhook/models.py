from django.db import models

class TwilioMessage(models.Model):
    message_sid = models.CharField(max_length=255, unique=True, db_index=True)
    account_sid = models.CharField(max_length=255, db_index=True)
    from_number = models.CharField(max_length=50)
    to_number = models.CharField(max_length=50)
    body = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)
    profile_name = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.from_number} To: {self.to_number} - SID: {self.message_sid}"
