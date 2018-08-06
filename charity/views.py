import json

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import CharityProfile, Campaign, CampaignItem, Tag


@csrf_exempt
def signup_submit(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    name = request.POST.get('name', None)
    charity_url = request.POST.get('charity_url', None)
    email = request.POST.get('email', None)
    bio = request.POST.get('bio', None)
    campaign_name = request.POST.get('campaign_name', None)
    user = User(username=username, password=password, email=email)
    user.set_password(password)
    user.save()
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
    print(campaign_id)
    if campaign_id is None:
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
        },
    )


@csrf_exempt
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

    charity_profile.update(**params['fields'])
    charity_profile = charity_profile[0]
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
    })


def charities(request):
    items =  CharityProfile.objects.filter(is_displayed=True)

    return render(
        request,
        'charities.html',
        {'user': request.user, 'items': items},
    )

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def delete_campaign_item(request, campaign_item_id):
    campaign_item = CampaignItem.objects.get(pk=campaign_item_id)
    campaign_item.delete()

    return JsonResponse({
        'success': True,
    })
