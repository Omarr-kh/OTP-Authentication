from django.db import models


class OTPCode(models.Model):
    phone = models.CharField(max_length=30)
    code = models.CharField(max_length=4)