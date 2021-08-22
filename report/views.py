from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from inonet.users.models import User
from posts.models import Post, Comment
from works.models import Work
from .models import Report, USER, POST, COMMENT, WORK

# Create your views here.
class UserReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = "posts/new.html"
    fields = [
        "report_subject"
    ]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.report_type = USER
        form.instance.user = User.objects.get(username=self.kwargs["username"])
        form.save()
        return JsonResponse({"status": "success"})

    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class PostReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = "posts/new.html"
    fields = [
        "report_subject"
    ]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.report_type = POST
        form.instance.post = Post.objects.get(uuid=self.kwargs["uuid"])
        form.save()
        return JsonResponse({"status": "success"})

    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class CommentReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = "posts/new.html"
    fields = [
        "report_subject"
    ]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.report_type = COMMENT
        form.instance.comment = Comment.objects.get(uuid=self.kwargs["uuid"])
        form.save()
        return JsonResponse({"status": "success"})

    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})

class WorkReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = "posts/new.html"
    fields = [
        "report_subject"
    ]

    def form_valid(self, form):
        form.instance.reporter = self.request.user
        form.instance.report_type = WORK
        form.instance.work = Work.objects.get(uuid=self.kwargs["uuid"])
        form.save()
        return JsonResponse({"status": "success"})

    def form_invalid(self, form):
        return JsonResponse({"status":"failed", 'errors': form._errors})
