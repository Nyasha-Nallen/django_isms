from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('STAFF', 'Staff'),
    ]
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default='ADMIN')
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.email
    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    #profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"
