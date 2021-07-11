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
        if work.user != self.request.user:
            raise PermissionDenied()
        form.instance.work = work
        return super().form_valid(form)

class NewFingerprintWorkView(TemplateView):
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
        works = Work.objects.filter(user=user)
        qs = FingerPrint.objects.none()
        for work in works:
            qs = qs | FingerPrint.objects.filter(work = work)
        return qs
    