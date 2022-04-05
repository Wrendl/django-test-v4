from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone, dateformat
import pytz


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, gender, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, gender=gender, date_of_birth=date_of_birth)

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=10, default='01.01.2000')
    # creation_time = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=1, default='M')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender', 'date_of_birth']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
