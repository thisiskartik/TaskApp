from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    phone_number = models.PositiveBigIntegerField(unique=True, 
                                                  validators=[MinValueValidator(1000000000),
                                                              MaxValueValidator(9999999999)])
    country_code = models.CharField(max_length=10, default="+91")
    otp = models.PositiveIntegerField(null=True, blank=True,
                                           validators=[MinValueValidator(100000),
                                                       MaxValueValidator(999999)])
    priority = models.PositiveSmallIntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['priority']

    objects = UserManager()

    def __str__(self):
        return f"{self.phone_number} | {self.priority}"
