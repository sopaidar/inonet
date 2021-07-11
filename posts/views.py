from django.db import models
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from inonet.users.models import User
from django.utils.translation import gettext_lazy as _

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = [
        "text",
        "image"
    ]
    template_name = "posts/new.html"


# Create your views here.
class Timeline(ListView):
    model = Post
    paginate_by = 20
    template_name = "posts/list.html"
    