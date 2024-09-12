from django.db import models
from django.utils import timezone
from datetime import timedelta


class OTPCode(models.Model):
    phone = models.CharField(max_length=30)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)
