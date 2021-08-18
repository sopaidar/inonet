from django.urls import path

from .views import (
    FingerprintCreateView,
    NewFingerprintWorkView,
    ValidateView,
    UserFingerprintsListView,
    FingerPrintDetailView
)


urlpatterns = [
    path("new/", view=FingerprintCreateView.as_view(), name="new-fingerprint"),
    path("new_work/", NewFingerprintWorkView.as_view(), name="new_work"),
    path("validate/", ValidateView.as_view(), name="validate"),
    path("user_fingerprints/<uuid:uuid>/", UserFingerprintsListView.as_view(), name="user-fingerprints"),
    path("detail/<uuid:uuid>/", FingerPrintDetailView.as_view(), name="fingerprint-detail"),

]
