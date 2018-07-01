import uuid

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CharityProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    # on_delete will also delete all linked data to that user
    name = models.CharField(max_length=200)
    charity_url = models.URLField()
    bio = models.TextField(null=True, blank=True, default=None)
    img_url = models.URLField(null=True, blank=True, default=None)
    money_raised = models.IntegerField(null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)

    def profile_url(self):
        return f'/charity/{self.name}/{self.id}/'
