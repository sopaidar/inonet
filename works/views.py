from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Work

# Create your views here.
class WorkCreateView(CreateView):
    model = Work
    template_name = "works/new.html"
    fields = [
        "title",
        "work_type",
        "description"
    ]
