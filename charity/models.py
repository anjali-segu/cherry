import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

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

    def campaign_goal(self):
        campaign = self.campaign_set.all()[0]
        return int(campaign.goal())

    def campaign_items(self):
        campaign = self.campaign_set.all()[0]
        return campaign.campaignitem_set.all()

    def __str__(self):
        return f'Charity Profile: {self.name} ({self.id})'


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    charityprofile = models.ForeignKey(CharityProfile, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def goal(self):
        """
        Should be the sum of the CampaignItem cost
        """
        total_cost = self.campaignitem_set.all().aggregate(Sum('item_cost'))['item_cost__sum']
        return total_cost

    def __str__(self):
        return f'Campaign: {self.charityprofile.name} ({self.id})'

class CampaignItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_cost = models.FloatField()
    item_description = models.TextField(null=True, blank=True, default=None)
    item_img_url = models.URLField(null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
