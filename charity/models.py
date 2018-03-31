import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CharityProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    charity_name = models.CharField(max_length=200)
    charity_email = models.EmailField()
    charity_url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
