import uuid
import math

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.
class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tag: {self.name}'

class CharityProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    # on_delete will also delete all linked data to that user
    name = models.CharField(max_length=200)
    charity_url = models.URLField()
    bio = models.TextField(null=True, blank=True, default=None)
    long_bio = models.TextField(null=True, blank=True, default=None)
    img_url = models.URLField(null=True, blank=True, default=None)
    money_raised = models.IntegerField(null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def bio_detail(self):
        return self.long_bio if self.long_bio is not None else self.bio

    def profile_url(self):
        return f'/charity/{self.name}/{self.id}/'

    def campaigns(self):
        return [campaign for campaign in self.campaign_set.all()]

    def total_goal(self):
        all_campaign_items = CampaignItem.objects.prefetch_related('campaign', 'campaign__charityprofile').filter(campaign__charityprofile_id=self.id)
        total_goal = all_campaign_items.aggregate(Sum('item_cost'))['item_cost__sum']
        return math.floor(total_goal)

    def campaign_items(self):
        campaign = self.campaign_set.all()[0]
        return campaign.campaignitem_set.all()

    def percent_goal(self):
        """
        Should return the percent of the goal achieved
        """
        total_desired = self.total_goal()
        if not total_desired:
            return 0

        percent_goal = math.floor(self.money_raised * 100 / total_desired)
        return percent_goal

    def all_tags(self):
        return self.tags.all()

    def tags_set(self):
        return set([tag.name for tag in self.all_tags()])

    def __str__(self):
        return f'Charity Profile: {self.name} ({self.id})'


class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    charityprofile = models.ForeignKey(CharityProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)

    def campaign_items(self):
        return [item for item in self.campaignitem_set.all()]

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

    def item_cost_formatted(self):
        return math.floor(self.item_cost)
