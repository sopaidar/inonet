import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
# Create your models here.

NL = _("پسند جدید")
NC = _("نظر جدید")
NF = _("دنبال کننده جدید")
NS = _("بازنشر جدید")
NT = _("بازنشر جدید (با متن)")
PL = _("پسند نظر جدید")
NOTIFICATION_TYPE_CHOICES = [
    (NL, _("پسند جدید")),
    (NC, _("نظر جدید")),
    (NF, _("دنبال کننده جدید")),
    (NS, _("بازنشر جدید")),
    (NT, _("بازنشر جدید (با متن)")),
    (PL, _("پسند نظر جدید"))
]

class Notification(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر اعلان"), on_delete=models.CASCADE, related_name="user")
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(_("نوع اعلان"), max_length=50, choices=NOTIFICATION_TYPE_CHOICES, default=NL)
    actor = models.ForeignKey("users.User", verbose_name=_("فعال‌کننده"), on_delete=models.CASCADE, related_name="actor")
    post = models.ForeignKey("posts.Post", verbose_name=_(""), on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey("posts.Comment", verbose_name=_(""), on_delete=models.CASCADE, null=True)
    date_time = models.DateTimeField(_("زمان"), auto_now=True)
    got = models.BooleanField(_("دریافت شده"), default=False)
    seen = models.BooleanField(_("مشاهده شده"), default=False)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return f"{self.notification_type} - فعال‌کننده: {self.actor.username} - کاربر: {self.user.username}"

    # def get_absolute_url(self):
    #     return reverse("Notification_detail", kwargs={"uuid": self.uuid})
