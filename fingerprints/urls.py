from django.urls import path

from .views import (
    FingerprintCreateView,
    NewFingerprintWorkView,
    ValidateView
)


urlpatterns = [
    path("new/", view=FingerprintCreateView.as_view(), name="new-fingerprint"),
    path("new_work/", NewFingerprintWorkView.as_view(), name="new_work"),
    path("validate/", ValidateView.as_view(), name="validate")

]