from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import CharityProfile, Campaign

# Create your views here.
# class CharityProfileDetail(View):
#
#     def get(self, charity_name, charity_id, **kwargs):
#         return render(
#             request,
#             'charity.html',
#             {'user': request.user},
#         )

@csrf_exempt
def signup_submit(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    name = request.POST.get('name', None)
    charity_url = request.POST.get('charity_url', None)
    email = request.POST.get('email', None)
    user = User(username=username, password=password, email=email)
    user.set_password(password)
    user.save()
    login(request, user)
    charity_profile = CharityProfile(user=user, name=name, charity_url=charity_url)
    charity_profile.save()
    campaign = Campaign(charityprofile=charity_profile)
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
    return render(
        request,
        'charity.html',
        {
            'user': request.user,
            'charity': charity,
            'charity_logged_in': charity_logged_in
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

    updated_fields = request.POST.dict()
    charity_profile = CharityProfile.objects.filter(pk=charity_id)
    charity_profile.update(**updated_fields)
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
