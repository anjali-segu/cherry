from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import CharityProfile

class CharityProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        '_user',
        'name',
        'charity_url',
        'bio',
        'img_url',
        'money_raised',
        'date_created'
    )

    list_display_links = ('id',)

    def _user(self, instance):
        link = reverse('admin:auth_user_change', args=[instance.user.id])

        return format_html('<a href="{link}" target="_blank">{username}</a>'.format(
            link=link,
            username=instance.user.username
        ))

# Register your models here.
admin.site.register(CharityProfile, CharityProfileAdmin)
