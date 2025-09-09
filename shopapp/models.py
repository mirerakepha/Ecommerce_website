from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)
    location = models.CharField(max_length=120, blank=True, null=True)
    delivery_center = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s profile"
