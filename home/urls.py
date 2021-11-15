from django.urls import path
from django.views.generic import TemplateView
from .views import (
    home,
)


urlpatterns = [
    path("", home, name="home"),
    path("blog/what-is-intellectual-property-مالکیت-فکری-چیست",
         TemplateView.as_view(template_name="pages/ip.html"), name="what_is_ip"),
    path("blog/types-of-intellectual-property-انواع-مالکیت-فکری",
         TemplateView.as_view(template_name="pages/classification.html"), name="types_of_ip"),
    path("blog/intellectual-property-Iran-مالکیت-فکری-در-ایران",
         TemplateView.as_view(template_name="pages/ipiran.html"), name="ip_Iran"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    path(
        "contact/", TemplateView.as_view(template_name="pages/contact.html"), name="contact"
    ),
    path(
        "policy/", TemplateView.as_view(template_name="pages/policy.html"), name="policy"
    ),
    path(
        "privacy/", TemplateView.as_view(template_name="pages/privacy.html"), name="privacy"
    ),
    path(
        "timestamp-certificate/", TemplateView.as_view(template_name="pages/timestamp_certificate.html"), name="timestamp_certificate"
    ),
    path(
        "register/", TemplateView.as_view(template_name="pages/register.html"), name="register"
    ),
    path(
        "blockchain-timestamp/", TemplateView.as_view(template_name="pages/blockchain_timestamp.html"), name="blockchain_timestamp"
    ),

    
]
