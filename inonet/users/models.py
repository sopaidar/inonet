from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for inonet."""

    #: First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_("نام"), blank=True, max_length=255)
    last_name = models.CharField(_("نام خانوادگی"), blank=True, max_length=255)
    avatar = models.ImageField(_("تصویر نمایه"), upload_to="avatars/", blank=True, null=True)
    followers = models.PositiveIntegerField(_("تعداد دنبال‌کنندگان"), default=0)
    likes = models.JSONField(_("لایک‌های کاربر"),default=dict)
    shares = models.JSONField(_("به‌اشتراک‌گذاری‌های کاربر"), default=dict)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
