from django.urls import path

from .views import (
    PostCreateView,
    Timeline
)


urlpatterns = [
    path("new/", PostCreateView.as_view(), name="new-post"),
    path("", view=Timeline.as_view(), name="timeline"),


]