from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt

from .models import CharityProfile

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

sample_charities = [
    {
        'name': 'Austin Pets Alive',
        'email': None,
        'password': None,
        'id': None,
        'url': 'https://www.austinpetsalive.org/',
        'bio': 'We maintain innovative programs designed to save animals from euthanasia',
        'image_url': 'https://pbs.twimg.com/profile_images/908381920207134721/cyz_nKaf_400x400.jpg',
        'money_raised': '300',
        'tags': [
            'animals',
            'shelter'
        ]
    },
    {
        'name': 'American Cancer Society',
        'email': None,
        'password': None,
        'id': None,
        'url': 'https://www.cancer.org/',
        'bio': 'Dedicated to helping people who face cancer. Learn about cancer research, patient services, early detection, treatment and education at cancer.org.',
        'image_url': 'https://i.forbesimg.com/media/lists/companies/american-cancer-society_416x416.jpg',
        'money_raised': '200',
        'tags': [
            'health',
            'cancer'
        ]
    },
    {
        'name': 'Scottish Rite Theater',
        'email': None,
        'password': None,
        'id': None,
        'url': 'http://scottishritetheater.org/about/',
        'bio': 'We maintain innovative programs designed to save animals from euthanasia',
        'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/j7PZ7AeRN5m3sMjlcePo2A/l.jpg',
        'money_raised': '100',
        'tags': [
            'children',
            'entertainment'
        ]
    },

]

def charities(request):
    items =  CharityProfile.objects.filter(is_displayed=True)

    return render(
        request,
        'charities.html',
        {'user': request.user, 'items': items},
    )
