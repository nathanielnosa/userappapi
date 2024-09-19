from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)  # Keep phone here if needed
    profile_pix = models.URLField(max_length=255)

    def __str__(self):
        return self.user.username