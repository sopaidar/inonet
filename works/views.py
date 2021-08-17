from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Work
from inonet.users.models import User
from fingerprints.models import FingerPrint
from posts.models import Post
from django.utils.translation import gettext_lazy as _

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

    def get_success_url(self):
        Post.objects.create(user=self.request.user, work=self.object, post_type=_("اثر جدید"))
        return super().get_success_url()


class WorkDetailView(LoginRequiredMixin, DetailView):
    model= Work
    template_name = "works/detail.html"
    slug_url_kwarg = "uuid"

    def get_object(self):
        work = Work.objects.get(uuid=self.kwargs["uuid"])
        return work

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fingerprints'] = FingerPrint.objects.filter(work=self.object).order_by("-pk")
        return context


class WorkImageUpdateView(LoginRequiredMixin, UpdateView):
    model= Work
    fields= ["work_image"]
    template_name = "works/detail.html"

    def get_object(self):
        work = Work.objects.get(uuid=self.kwargs["uuid"])
        return work

    def form_valid(self, form):
        if self.object.user != self.request.user:
            raise PermissionError
        form.save()
        return JsonResponse({'msg': 'success', 'new_pic_url': self.object.work_image.url})

    def form_invalid(self, form):
        return JsonResponse({'msg': 'failed', 'errors': form._errors})

        
class UserWorksListView(LoginRequiredMixin ,ListView):
    model = Work
    template_name = "users/user_works.html"
    paginate_by = 20
    def get_queryset(self):
        qs = Work.objects.filter(user=User.objects.get(uuid=self.kwargs['uuid']))
        return qs
    
