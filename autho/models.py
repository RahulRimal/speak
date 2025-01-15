from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class AuthProvider(models.TextChoices):
        AUTH_PROVIDER_SELF = "self"
        AUTH_PROVIDER_GOOGLE = "google"

        def __str__(self):
            return self.value

    class Gender(models.TextChoices):
        MALE = "male"
        FEMALE = "female"
        OTHER = "other"

    auth_provider = models.CharField(
        max_length=20,
        choices=AuthProvider,
        default=AuthProvider.AUTH_PROVIDER_SELF,
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender,
        default=Gender.MALE,
    )

    image = models.FileField(upload_to="users", null=True, blank=True)
