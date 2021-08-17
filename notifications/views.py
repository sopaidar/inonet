from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.http import JsonResponse
from .models import Notification
# Create your views here.

class NotificationsListView(ListView):
    model = Notification
    template_name = "notifications/new.html"
    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user, seen=False).order_by("-pk")
        if qs.count() > 0:
            for notification in qs:
                notification.got = True
                notification.save()
            return qs
        qs = Notification.objects.filter(user=self.request.user).order_by("-pk")[0:5]
        return qs


class AllNotificationsListView(ListView):
    model = Notification
    template_name = "notifications/all.html"
    paginate_by = 20
    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        return qs
    
class SeenNotification(View):
    def post(self, request):
        user = self.request.user
        notifications = Notification.objects.filter(user=user, seen=False, got=True)
        for notification in notifications:
            notification.seen = True
            notification.save()
        return JsonResponse({"status":"success"})
