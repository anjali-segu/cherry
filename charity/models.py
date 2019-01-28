import uuid
import math

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

DEFAULT_IMAGE = '/static/cherry_giver_logo_default.png'

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
    charity_url = models.URLField(null=True, blank=True, default=None)
    bio = models.TextField(null=True, blank=True, default=None)
    long_bio = models.TextField(null=True, blank=True, default=None)
    img_url = models.URLField(null=True, blank=True, default=None)
    # money_raised = models.IntegerField(null=True, blank=True, default=None)
    date_created = models.DateTimeField(auto_now_add=True)
    is_displayed = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_password_reset = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def formatted_image(self):
        return self.img_url if self.img_url else DEFAULT_IMAGE

    def bio_detail(self):
        return self.long_bio if self.long_bio else self.bio

    def profile_url(self):
        return f'/charity/{self.name}/{self.id}/'

    def campaigns(self):
        return [campaign for campaign in self.campaign_set.all()]

    def all_campaign_items(self):
        return CampaignItem.objects.prefetch_related('campaign', 'campaign__charityprofile').filter(campaign__charityprofile_id=self.id)

    def total_goal(self):
        all_campaign_items = self.all_campaign_items()
        total_goal = all_campaign_items.aggregate(Sum('item_cost'))['item_cost__sum']
        return math.floor(total_goal) if total_goal else 0

    def has_campaign(self):
        return len(self.campaign_set.all()) > 0

    def has_campaign_items(self):
        return len(self.all_campaign_items()) > 0

    def campaign_items(self):
        campaign = self.campaign_set.all()[0]
        return campaign.campaignitem_set.all()

    def money_raised(self):
        money_raised_in_cents = self.donation_set.all().aggregate(Sum('amount'))['amount__sum']
        if money_raised_in_cents is None:
            return 0

        return math.floor(money_raised_in_cents / 100)

    def percent_goal(self):
        """
        Should return the percent of the goal achieved
        """
        total_desired = self.total_goal()
        if not total_desired:
            return 0

        money_raised = self.money_raised()
        if not money_raised:
            return 0

        percent_goal = math.floor(money_raised * 100 / total_desired)
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

    def formatted_name(self):
        return self.name.title()

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
