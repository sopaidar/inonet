from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Follow
# Create your views here.
class FollowCreateView(LoginRequiredMixin ,CreateView):
    model = Follow
    template_name = "posts/new.html"
    fields = ["followed"]
    def form_valid(self, form):
        user = self.request.user
        following_status = True
        try:
            Follow = Follow.objects.get(user=user, post=post)
            Follow.Followd = True
            Follow.save()
            post.Follows = post.Follows + 1
            post.save()
            user.Follows["Follows"].append(post.pk)
            user.save()
            return JsonResponse({"status":"success"})
        except Follow.DoesNotExist:
            pass
        try:
            form.instance.user= user
            form.instance.post = post
            form.save()
        except IntegrityError:
            return JsonResponse({"status":"failed", 'errors': "Followd before"})
        post.Follows = post.Follows + 1
        post.save()
        if "Follows" in user.Follows:
            user.Follows["Follows"].append(post.pk)
        else:
            user.Follows = {"Follows":[post.pk]}
            user.save()
        return JsonResponse({"status":"success"})
    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

