from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, render_to_response

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('charity')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def index(request):
    return render(
        request,
        'index.html',
        {'user': request.user},
    )

def charities(request):
    return render(
        request,
        'charities.html',
        {'user': request.user},
    )

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
