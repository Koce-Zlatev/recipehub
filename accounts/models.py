from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    bio = models.TextField(blank=True)
    def __str__(self):
        return self.display_name or self.user.username
