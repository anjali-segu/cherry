from django.shortcuts import render
from django.views.generic import View

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
def charity(request, charity_name, charity_id):
    print(charity_id, charity_name)
    charity = CharityProfile.objects.get(pk=charity_id)
    return render(
        request,
        'charity.html',
        {
            'user': request.user,
            'charity': charity,
        },
    )
