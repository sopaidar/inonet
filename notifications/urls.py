from django.urls import path
from .views import NotificationsListView, AllNotificationsListView, SeenNotification


urlpatterns = [
    path("new/", NotificationsListView.as_view(), name="new-notifications"),
    path("all/", AllNotificationsListView.as_view(), name="all-notifications"),
    path("seen/", SeenNotification.as_view(), name="seen-notifications")

]
