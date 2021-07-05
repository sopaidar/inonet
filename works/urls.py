from django.urls import path

from .views import (
    WorkCreateView,
)


urlpatterns = [
    path("new/", view=WorkCreateView.as_view(), name="new_work"),

]