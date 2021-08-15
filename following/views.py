from django.shortcuts import render
from django.db import IntegrityError
from django.views.generic.edit import CreateView, UpdateView
import json
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from inonet.users.models import User
from notifications.models import Notification
from .models import Follow
from django.utils.translation import gettext_lazy as _

# Create your views here.

class UserFollowings(LoginRequiredMixin, View):
    def get(self, request):

        data = self.request.user.followings    
        return JsonResponse({"status":"success", "followings": data})

class FollowCreateView(LoginRequiredMixin ,CreateView):
    model = Follow
    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        followed = User.objects.get(username=self.kwargs["username"]) 
        user = self.request.user
        try:
            follow = Follow.objects.get(follower=user, followed=followed)
            if follow.following_status==True:
                return JsonResponse({"status":"failed", 'errors': "followed before"})
            follow.following_status=True
            follow.save()
            followed.followers = followed.followers + 1
            followed.save()
            user.followings["followings"].append(followed.username)
            user.save()
            notification = Notification(actor=user, user=followed, notification_type=_("دنبال کننده جدید"))
            notification.save()
            return JsonResponse({"status":"success"})
        except Follow.DoesNotExist:
            pass
        try:
            form.instance.follower = user
            form.instance.followed = followed
            form.instance.following_status = True
            form.save()
        except IntegrityError:
            return JsonResponse({"status":"failed", 'errors': "followed before"})
        followed.followers = followed.followers + 1
        followed.save()
        if "followings" in user.followings:
            user.followings["followings"].append(followed.username)
        else:
            user.followings = {"followings":[followed.username]}
        user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class UnfolowUpdateView(LoginRequiredMixin ,UpdateView):
    model = Follow

    def get_object(self):
        
        user= self.request.user
        followed = User.objects.get(username=self.kwargs["username"])     
        
        try:
            follow = Follow.objects.get(follower=user, followed=followed)
        except Follow.DoesNotExist:
            return JsonResponse({"status":"failed", "errors": "didn't followed before"})
        return follow

    template_name = "posts/new.html"
    fields = []
    def form_valid(self, form):
        followed = self.object.followed
        user = self.request.user
        if self.object.follower != user:
            raise PermissionError
        if form.instance.followed == False:
            return JsonResponse({"status":"failed", 'errors': "unfollowed before"})
        form.instance.following_status = False
        form.save()
        followed.followers = followed.followers + 1
        followed.save()
        user.followings["followings"] = list(filter((followed.username).__ne__, user.followings["followings"]))
        user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

