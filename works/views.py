from django.db import models
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Work
from fingerprints.models import FingerPrint

# Create your views here.
class WorkCreateView(LoginRequiredMixin, CreateView):
    model = Work
    template_name = "works/new.html"
    fields = [
        "title",
        "work_type",
        "description"
    ]
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class WorkDetailView(DetailView):
    model= Work
    template_name = "works/detail.html"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fingerprints'] = FingerPrint.objects.filter(work=self.object).order_by("-pk")
        return context


class WorkImageUpdateView(LoginRequiredMixin, UpdateView):
    model= Work
    fields= ["work_image"]
    template_name = "works/detail.html"

    def form_valid(self, form):
        if self.object.user != self.request.user:
            raise PermissionError
        form.save()
        return JsonResponse({'msg': 'success', 'new_pic_url': self.object.work_image.url})

    def form_invalid(self, form):
        return JsonResponse({'msg': 'failed', 'errors': form._errors})

        