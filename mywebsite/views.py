from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from charity.models import CharityProfile

@csrf_exempt
def login_route(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request,user)
        charity_profile = CharityProfile.objects.get(user=user)
        return JsonResponse({
            'success':user is not None,
            'charity_profile_name': charity_profile.name,
            'charity_profile_id': charity_profile.id,

        })
    return JsonResponse({
        'success': False,
    })

@csrf_exempt
def logout_route(request):
    logout(request)
    return JsonResponse({'success':True})

def index(request):
    return render(
        request,
        'index.html',
        {'user': request.user},
    )

# NOTE: this is temporary until we create the db table
# sample_charities = [
#     {
#         'title': 'Austin Pets Alive',
#         'url': 'https://www.austinpetsalive.org/',
#         'bio': 'We maintain innovative programs designed to save animals from euthanasia',
#         'image_url': 'https://pbs.twimg.com/profile_images/908381920207134721/cyz_nKaf_400x400.jpg',
#         'money_raised': '300',
#         'tags': [
#             'animals',
#             'shelter'
#         ]
#     },
#     {
#         'title': 'American Cancer Society',
#         'url': 'https://www.cancer.org/',
#         'bio': 'Dedicated to helping people who face cancer. Learn about cancer research, patient services, early detection, treatment and education at cancer.org.',
#         'image_url': 'https://i.forbesimg.com/media/lists/companies/american-cancer-society_416x416.jpg',
#         'money_raised': '200',
#         'tags': [
#             'health',
#             'cancer'
#         ]
#     },
#     {
#         'title': 'Scottish Rite Theater',
#         'url': 'http://scottishritetheater.org/about/',
#         'bio': 'We maintain innovative programs designed to save animals from euthanasia',
#         'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/j7PZ7AeRN5m3sMjlcePo2A/l.jpg',
#         'money_raised': '100',
#         'tags': [
#             'children',
#             'entertainment'
#         ]
#     },
#
# ]

# def charities(request):
#     return render(
#         request,
#         'charities.html',
#         {'user': request.user, 'items': sample_charities},
#     )


# ^ move that into views.py of charity folder


# def charity(request, charity_name, charity_id):
#     print(charity_id, charity_name)
#     charity = Charity.object.get(pk=charity_id)
#     return render(
#         request,
#         'charity.html',
#         {
#             'user': request.user,
#             'charity': charity,
#         },
#     )
