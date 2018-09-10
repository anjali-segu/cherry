import uuid

from django.db import models

from charity.models import CharityProfile


# Create your models here.
class Donation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount=models.FloatField()
    charityprofile=models.ForeignKey(CharityProfile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Donation: {self.amount}'
