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
            'is_admin': user.is_staff,
        })
    return JsonResponse({
        'success': False,
    })

@csrf_exempt
def logout_route(request):
    logout(request)
    return JsonResponse({'success':True})

def index(request):
    try:
        featured_charity = CharityProfile.objects.filter(is_featured=True)[0]
    except(IndexError):
        featured_charity = None

    return render(
        request,
        'index.html',
        {
            'user': request.user,
            'featured_charity': featured_charity,
            'should_render_featured_charity': featured_charity is not None,
        },
    )

def team(request):
    return render(
        request,
        'team.html',
    )
