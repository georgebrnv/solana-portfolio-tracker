from django.db import models

class UserProfileImages(models.Model):
    image = models.ImageField(upload_to='user_profile/profile_images/', default='user_profile/default_profile_img/default_profile_pic.jpeg')

    def __str__(self, *args, **kwargs):
        return f"{self.image}"