from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import FingerPrint
from works.models import Work
from inonet.users.models import User
from posts.models import Post
from django.utils.translation import gettext_lazy as _

# Create your views here.

class FingerprintCreateView(LoginRequiredMixin, CreateView):
    model = FingerPrint
    template_name = "fingerprints/new.html"
    fields = [
        "fingerprint",
        "post_text",
    ]

    def form_valid(self, form):
        work = Work.objects.get(pk=self.request.GET['id'])
        print(self.request.GET['id'])
        user = self.request.user
        if work.user != user:
            raise PermissionDenied()
        form.instance.user = user
        form.instance.work = work
        return super().form_valid(form)

    def get_success_url(self):
        Post.objects.create(user=self.request.user, fingerprint=self.object, post_type=_("گواهی زمانی جدید"), text=self.object.post_text)
        return super().get_success_url()

class NewFingerprintWorkView(LoginRequiredMixin ,TemplateView):
    template_name = "fingerprints/new_work.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_works"] = Work.objects.filter(user=self.request.user).order_by("-pk")
        return context



class ValidateView(View):

    def get(self, request):
        return render(request, "fingerprints/validate.html")

    def post(self, request):
        fingerprint = self.request.POST.get("fingerprint")
        try:
            fp = FingerPrint.objects.get(fingerprint=fingerprint)
            if self.request.user.is_authenticated:
                return JsonResponse(
                    {
                        "status": "found",
                        "fingerprint": fp.fingerprint,
                        "date": [fp.date_time.year, fp.date_time.month, fp.date_time.day],
                        "time": f"{fp.date_time.hour}:{fp.date_time.minute}:{fp.date_time.second}",
                        "id": fp.pk, "work": fp.work.pk,
                        "user":{"username":fp.work.user.username, "first_name":fp.work.user.first_name, "last_name": fp.work.user.last_name}
                    }
                )
            return JsonResponse({"status": "found"})
        except FingerPrint.DoesNotExist:
            return JsonResponse({"status": "not found"})
        


class UserFingerprintsListView(LoginRequiredMixin ,ListView):
    model = Work
    template_name = "users/user_Fingerprints.html"
    paginate_by = 20

    def get_queryset(self):
        user = User.objects.get(pk = self.kwargs['pk'])
        qs = FingerPrint.objects.filter(user = user)
        return qs
    