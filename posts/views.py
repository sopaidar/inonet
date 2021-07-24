from django.db import IntegrityError
from django.db.models.fields import DateTimeField, UUIDField
from django.db.models.fields.related import ForeignKey
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Like, Post, Share, Comment
from inonet.users.models import User
import json
from django.utils.translation import gettext_lazy as _

class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    fields = [
        "text",
        "image",
        "shared_post",
        "draft"
    ]
    template_name = "posts/new.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.shared_post:
            form.instance.post_type = _("خبر به اشتراک‌گذاری شده")
        else:
            form.instance.post_type = _("خبر جدید")
        form.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})


# Create your views here.
class Timeline(ListView):
    model = Post
    paginate_by = 20
    template_name = "posts/list.html"
    def get_queryset(self):
        qs = Post.objects.filter(draft=False).order_by("-pk")
        return qs
    

class UserLikes(View):
    def get(self, request):
        likes = self.request.user.likes
        shares = self.request.user.shares
        return JsonResponse({"status": "success", "likes": likes, "shares": shares})

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
        if "likes" in user.likes:
            user.likes["likes"].append(post.pk)
        else:
            user.likes = {"likes":[post.pk]}
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


class ShareCreateView(LoginRequiredMixin ,CreateView):
    model = Share
    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        try:
            share = Share.objects.get(user=user, post=post)
            share.shared = True
            share.save()
            post.shares = post.shares + 1
            post.save()
            user.shares["shares"].append(post.pk)
            user.save()
            return JsonResponse({"status":"success"})
        except Share.DoesNotExist:
            pass
        try:
            form.instance.user= user
            form.instance.post = post
            form.save()
        except IntegrityError:
            return JsonResponse({"status":"failed", 'errors': "shared before"})
        post.shares = post.shares + 1
        post.save()
        if "shares" in user.shares:
            user.shares["shares"].append(post.pk)
        else:
            user.shares = {"shares":[post.pk]}
            user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class UnShareUpdateView(LoginRequiredMixin ,UpdateView):
    model = Share
    def get_object(self):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        try:
            share = Share.objects.get(user=user, post=post)
        except Share.DoesNotExist:
            return JsonResponse({"status":"failed", "errors": "didn't share before"})
        return share
    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        post = Post.objects.get(pk=self.kwargs["pk"])
        user = self.request.user
        if self.object.user != user:
            raise PermissionError
        if form.instance.shared == False:
            return JsonResponse({"status":"failed", 'errors': "disshared before"})
        form.instance.shared = False
        form.save()
        post.shares = post.shares - 1
        post.save()
        user.shares["shares"] = list(filter((post.pk).__ne__, user.shares["shares"]))
        user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class CommentCreateView(LoginRequiredMixin ,CreateView):
    model = Comment
    fields = [
        "text",
        "answered_to",

    ]
    template_name = "posts/new.html"
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs["pk"])
        form.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

# drf
class PostComments(LoginRequiredMixin, View):
    def get(self, request, pk):

        data = serializers.serialize("json", Comment.objects.filter(post=Post.objects.get(pk=pk)))
        data_json = json.loads(data)
        for comment in data_json:
            user_pk = comment["fields"]["user"]
            user= User.objects.get(pk=user_pk)
            comment["fields"]["user"] = {"username": user.username, "first_name": user.first_name, "last_name": user.last_name, "avatar_url": user.avatar.url}

        data_json = json.dumps(data_json)


        return HttpResponse(data_json)
