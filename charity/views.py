import json
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.db.utils import IntegrityError

from .models import CharityProfile, Campaign, CampaignItem, Tag


def _url_with_scheme(url):
    parsed_result = urlparse(url)
    if 'http' not in parsed_result.scheme:
        return 'https://' + parsed_result.geturl()

    return url


def signup_submit(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    name = request.POST.get('name', None)
    charity_url = request.POST.get('charity_url', None)
    if charity_url:
        charity_url = _url_with_scheme(charity_url)
    email = request.POST.get('email', None)
    bio = request.POST.get('bio', None)
    campaign_name = request.POST.get('campaign_name', None)

    try:
        user = User(username=username, password=password, email=email)
        user.set_password(password)
        user.save()
    except(IntegrityError):
        return JsonResponse({'success': False, 'message': 'Username already exists.'})

    login(request, user)
    charity_profile = CharityProfile(user=user, name=name, charity_url=charity_url, bio=bio)
    charity_profile.save()
    campaign = Campaign(charityprofile=charity_profile, name=campaign_name)
    campaign.save()
    return JsonResponse({
        'user_id': user.id,
        'charity_profile_id': charity_profile.id,
        'charity_profile_name': charity_profile.name,
        'success': True,

    })


def signup(request):
    return render(
        request,
        'signup.html',
        {
            'user': request.user,
        },
    )


def charity(request, charity_name, charity_id):
    charity_logged_in = (
        request.user.is_authenticated and
        str(request.user.charityprofile.id) == charity_id
    )

    charity = CharityProfile.objects.get(pk=charity_id)

    campaign_id = request.GET.get('campaign_id')
    if not charity.has_campaign():
        campaign = None
    elif campaign_id is None:
        campaign = charity.campaign_set.all()[0]
    else:
        campaign = Campaign.objects.get(pk=campaign_id)

    charity_tag_set = charity.tags_set()
    all_tags = []
    for tag in Tag.objects.order_by('name').all():
        all_tags.append({
            'name': tag.name,
            'checked': 'checked' if tag.name in charity_tag_set else ''
        })

    return render(
        request,
        'charity.html',
        {
            'user': request.user,
            'charity': charity,
            'all_tags': all_tags,
            'charity_logged_in': charity_logged_in,
            'campaign': campaign,
            'is_password_reset': request.GET.get('reset_password'),
        },
    )


def charity_update(request, charity_name, charity_id):
    charity_logged_in = (
        request.user.is_authenticated and
        str(request.user.charityprofile.id) == charity_id
    )

    if not charity_logged_in:
        return JsonResponse({
            'success': False,
        })

    params = json.loads(request.body)
    charity_profile = CharityProfile.objects.filter(pk=charity_id)
    redirect_url = charity_profile[0].profile_url()

    fields = params['fields']
    if 'charity_url' in fields:
        fields['charity_url'] = _url_with_scheme(fields['charity_url'] )

    user_fields = params['user_fields']
    if 'email' in user_fields:
        request.user.email = user_fields['email']
        request.user.save()

    if (
        'password' in user_fields and
        'password_repeat' in user_fields and
        user_fields['password'] == user_fields['password_repeat'] and
        len(user_fields['password']) >= 8 and
        len(user_fields['password_repeat']) >= 8
    ):
        request.user.set_password(user_fields['password'])
        request.user.save()
        charity_profile.update(is_password_reset=False)
        login(request, request.user)

    charity_profile.update(**fields)
    charity_profile = charity_profile[0]
    # In case the user updates the account without changing the password
    # when it has been reset via email
    if charity_profile.is_password_reset:
        redirect_url = f'{redirect_url}?reset_password=true'

    charity_tag_set = charity_profile.tags_set()
    # Update tags based on tags param
    for tag_name, should_tag in params['tags'].items():
        # Only add tag if tag_name from form is True and tag_name is not in charity's tags
        print(tag_name, should_tag)
        if should_tag and tag_name not in charity_tag_set:
            charity_profile.tags.add(Tag.objects.get(name=tag_name))
        # Only remove tag if if tag_name from form is False and the tag_name is currently in charity's tags
        elif should_tag == False and tag_name in charity_tag_set:
            charity_profile.tags.remove(Tag.objects.get(name=tag_name))

    return JsonResponse({
        'success': True,
        'redirect_url': redirect_url
    })

def charities(request):
    tag = request.GET.get('tag')
    name = request.GET.get('name')
    if tag:
        items = CharityProfile.objects.filter(
            is_displayed=True,
            tags__name__icontains=tag
        )
    elif name:
        items = CharityProfile.objects.filter(
            is_displayed=True,
            name__icontains=name
        )
    else:
        items = CharityProfile.objects.filter(is_displayed=True)

    return render(
        request,
        'charities.html',
        {'user': request.user, 'items': items, 'no_items': len(items) <= 0},
    )

def create_campaign(request):
    form_data = request.POST.dict()
    print(form_data)
    charity_profile = CharityProfile.objects.get(pk=form_data['charity_id'])

    campaign = Campaign(
        name=form_data['new_campaign_name'],
        charityprofile=charity_profile,
    )
    campaign.save()

    return JsonResponse({
        'success': True,
    })

def add_campaign_item(request, campaign_id):
    campaign = Campaign.objects.get(pk=campaign_id)

    campaign_item = CampaignItem(
        campaign=campaign,
        **request.POST.dict()
    )
    campaign_item.save()

    return JsonResponse({
        'success': True,
    })

def delete_campaign_item(request, campaign_item_id):
    campaign_item = CampaignItem.objects.get(pk=campaign_item_id)
    campaign_item.delete()

    return JsonResponse({
        'success': True,
    })
# This is new!
def delete_campaign(request, campaign_id):
    campaign = Campaign.objects.get(pk=campaign_id)
    campaign.delete()

    return JsonResponse({
        'success': True,
    })
