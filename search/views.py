from django.shortcuts import render
from django.views.generic.base import View
from inonet.users.models import User
from works.models import Work
from django.http import JsonResponse

# Create your views here.
class Search(View):
    def get(self, request):
        q = request.GET.get('q')

        return JsonResponse({"query": q})
