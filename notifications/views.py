from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Notification
# Create your views here.

class NotificationsListView(ListView):
    model = Notification
    template_name = "notifications/new.html"
    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user, seen=False).order_by("-pk")
        if qs.count() > 0:
            return qs
        qs = Notification.objects.filter(user=self.request.user).order_by("-pk")[0:10]
        return qs
        

class AllNotificationsListView(ListView):
    model = Notification
    template_name = "notifications/all.html"
    paginate_by = 20
    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user)
        return qs
        
        
    
