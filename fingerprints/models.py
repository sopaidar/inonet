from django.db import models
from django.db.models.base import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class FingerPrint(models.Model):

    work = models.ForeignKey("works.Work", verbose_name=_("اثر "), on_delete=models.CASCADE, related_name="fingerprintwork")
    fingerprint = models.CharField(_("اثرانگشت"), max_length=255)
    date_time = models.DateTimeField(_("تاریخ و زمان ثبت"), auto_now=True)
    registered_on_list_blockchain = models.BooleanField(_("ثبت شده در بلاکچین به صورت گروهی"))

    class Meta:
        verbose_name = _("FingerPrint")
        verbose_name_plural = _("FingerPrints")

    def __str__(self):
        return self.work.title

    def get_absolute_url(self):
        return reverse("FingerPrint_detail", kwargs={"pk": self.pk})
