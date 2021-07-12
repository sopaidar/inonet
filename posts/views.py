from django.db import models
from django.db import IntegrityError
from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Like, Post
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

class UserLikes(View):
    def get(self, request):
        likes = self.request.user.likes
        return JsonResponse({"status": "success", "likes": likes})

class LikeCreateView(LoginRequiredMixin ,CreateView):
    model = Like
    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        try:
            like = Like.objects.get(user=user, post=post)
            like.liked = True
            like.save()
            post.likes = post.likes + 1
            post.save()
            user.likes["likes"].append(post.pk)
            user.save()
            return JsonResponse({"status":"success"})
        except Like.DoesNotExist:
            pass
        try:
            form.instance.user= user
            form.instance.post = post
            form.save()
        except IntegrityError:
            return JsonResponse({"status":"failed", 'errors': "liked before"})
        post.likes = post.likes + 1
        post.save()
        user.likes["likes"].append(post.pk)
        user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class DisLikeUpdateView(LoginRequiredMixin ,UpdateView):
    model = Like
    def get_object(self):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        try:
            like = Like.objects.get(user=user, post=post)
        except Like.DoesNotExist:
            return JsonResponse({"status":"failed", "errors": "didn't like before"})
        return like
    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        if self.object.user != user:
            raise PermissionError
        if form.instance.liked == False:
            return JsonResponse({"status":"failed", 'errors': "disliked before"})
        form.instance.liked = False
        form.save()
        post.likes = post.likes - 1
        post.save()
        user.likes["likes"] = list(filter((post.pk).__ne__, user.likes["likes"]))
        user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})