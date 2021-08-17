from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for inonet."""

    #: First and last name do not cover name patterns around the globe
    first_name = models.CharField(_("نام"), blank=True, max_length=255)
    last_name = models.CharField(_("نام خانوادگی"), blank=True, max_length=255)
    bio = models.TextField(_("درباره من"), max_length=255, null=True, blank=True)
    avatar = models.ImageField(_("تصویر نمایه"), upload_to="avatars/", blank=True, null=True)
    followers = models.PositiveIntegerField(_("تعداد دنبال‌کنندگان"), default=0)
    likes = models.JSONField(_("لایک‌های کاربر"),default=dict)
    shares = models.JSONField(_("بازنشر‌های کاربر"), default=dict)
    followings = models.JSONField(_("کاربران فالو شده"), default=dict)
    notification_status = models.PositiveIntegerField(_("وضعیت اعلان‌ها"), default=0)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
