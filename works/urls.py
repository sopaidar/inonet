from django.urls import path

from .views import (
    WorkCreateView,
    WorkDetailView,
    WorkImageUpdateView,
    UserWorksListView
)


urlpatterns = [
    path("new/", view=WorkCreateView.as_view(), name="new_work"),
    path("<uuid:uuid>/", view=WorkDetailView.as_view(), name="work-detail"),
    path("<uuid:uuid>/upload_image/", WorkImageUpdateView.as_view(), name="upload-work-image"),
    path("user_works/<uuid:uuid>/", UserWorksListView.as_view(), name="user-works")

]