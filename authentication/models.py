from django.db import models
from django.contrib.auth.models import AbstractUser

from user_profile.models import UserProfileImages

# Create your models here.
class UserAuth(AbstractUser):
    # AbstractUser class fields are predefined, add additional ones below.
    profile_image = models.OneToOneField(to=UserProfileImages, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        if not self.profile_image:
            default_profile_image = UserProfileImages.objects.create()
            self.profile_image = default_profile_image
        super().save(*args, **kwargs)