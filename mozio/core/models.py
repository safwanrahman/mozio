from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import timezone

from .validators import phone_number_validator


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(validators=[phone_number_validator], blank=True, max_length=17)
    language = models.CharField(choices=settings.LANGUAGES, max_length=10, default="en-US")
    currency = models.CharField(choices=settings.CURRENCIES, max_length=10, default="USD")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "password"]

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    # This could be Django GIS PolygonField, but we are making queries in the Elasticsearch
    # So storing in JSON is enough.
    area = JSONField()
