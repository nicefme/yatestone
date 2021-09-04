from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    #first_name = models.CharField(max_length=150)
    #last_name = models.CharField(max_length=150)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
