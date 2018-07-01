from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import CharityProfile

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
        'money_raised',
        'date_created',

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

# Register your models here.
admin.site.register(CharityProfile, CharityProfileAdmin)
