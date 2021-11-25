from django.db import models
from django.conf import settings

# Делаем, что бі почта біла уникальной
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%y/%m/%d', blank=True, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'