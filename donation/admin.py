from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Donation

class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'amount',
        '_charity_profile_url',
        'date_created',
    )

    list_display_links = ('id',)

    def _charity_profile_url(self, instance):
        link = reverse('admin:charity_charityprofile_change', args=[instance.charityprofile.id])

        return format_html(
            f'<a href="{link}" target="_blank">{instance.charityprofile.name}</a>'
        )

# Register your models here.
admin.site.register(Donation, DonationAdmin)
