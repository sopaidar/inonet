from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

NL = "پسند جدید"
NC = "نظر جدید"
NF = "دنبال کننده جدید"

class Notification(models.Model):

    notification_type = models.CharField(_("نوع اعلان"), max_length=50)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Notification_detail", kwargs={"pk": self.pk})
