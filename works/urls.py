from django.urls import path

from .views import (
    WorkCreateView,
    WorkDetailView,
    WorkImageUpdateView
)


urlpatterns = [
    path("new/", view=WorkCreateView.as_view(), name="new_work"),
    path("<int:pk>/", view=WorkDetailView.as_view(), name="work-detail"),
    path("<int:pk>/upload_image/", WorkImageUpdateView.as_view(), name="upload-work-image")

]