from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import CharityProfile, Campaign, CampaignItem, Tag

class CharityProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '_user',
        'name',
        'is_displayed',
        'charity_url',
        '_profile_url',
        'bio',
        'img_url',
        # 'money_raised',
        'date_created',
        'is_featured'

    )

    list_display_links = ('id',)

    def _user(self, instance):
        link = reverse('admin:auth_user_change', args=[instance.user.id])

        return format_html(
            f'<a href="{link}" target="_blank">{instance.user.username}</a>'
        )

    def _profile_url(self, instance):
        return format_html(
            f'<a href="{instance.profile_url()}">{instance.profile_url()}</a>'
        )


class CampaignAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '_charityprofile',
        'goal',
        'date_created',
    )

    def _charityprofile(self, instance):
        link = reverse('admin:charity_charityprofile_change', args=[instance.charityprofile.id])

        return format_html(
            f'<a href="{link}" target="_blank">{instance.charityprofile.name}</a>'
        )

class CampaignItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '_campaign',
        'item_name',
        'item_cost',
        'item_img_url',
        'date_created',
    )

    def _campaign(self, instance):
        link = reverse('admin:charity_campaign_change', args=[instance.campaign.id])

        return format_html(
            f'<a href="{link}" target="_blank">{instance.campaign.id}</a>'
        )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'date_created',
    )


# Register your models here.
admin.site.register(Tag, TagAdmin)
admin.site.register(CharityProfile, CharityProfileAdmin)
admin.site.register(Campaign, CampaignAdmin)
admin.site.register(CampaignItem, CampaignItemAdmin)
