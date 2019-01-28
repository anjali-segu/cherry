from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse
from charity.models import CharityProfile
from mywebsite.emails import send_password_reset_email

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
            'is_password_reset': charity_profile.is_password_reset,
        })
    return JsonResponse({
        'success': False,
    })

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

def forget_password(request):
    email = request.POST.get('email', None)
    if email is None:
        return JsonResponse({'success': False, 'message': '"email" parameter not found in request'})

    # Find the user with the given email
    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'email "{email}" does not match any account'})

    # Send an email with new credentials
    send_password_reset_email(user)

    return JsonResponse({'success': True})
