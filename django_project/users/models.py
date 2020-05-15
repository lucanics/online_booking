from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # if user is deleted delete the profile also (but not the other way round)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    vorname = models.CharField(max_length=100, default="hans")
    nachname = models.CharField(max_length=100, default="max")
    adresse = models.TextField(max_length=500, default="gasse")
    telefonnummer = models.CharField(max_length=20, default=1234)
    email = models.EmailField(max_length=50, default="default@default.com")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # parent's classe's save function

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300: # resize image if it is too large
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)