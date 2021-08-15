from django.urls import path
from .views import NotificationsListView, AllNotificationsListView


urlpatterns = [
    path("new/", NotificationsListView.as_view(), name="new-notifications"),
    path("all/", AllNotificationsListView.as_view(), name="all-notifications")
]
