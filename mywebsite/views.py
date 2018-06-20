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

# NOTE: this is temporary until we create the db table
sample_charities = [
    {
        'title': 'Austin Pets Alive',
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
        'title': 'American Cancer Society',
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
        'title': 'Scottish Rite Theater',
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
    return render(
        request,
        'charities.html',
        {'user': request.user, 'items': sample_charities},
    )


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
