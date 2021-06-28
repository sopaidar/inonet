from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Work(models.Model):

    title = models.CharField(_("عنوان"), max_length=100)
    fingerprint= models.CharField(_("اثرانگشت"), max_length=100)
    work_type= models.CharField(_("نوع اثر"), max_length=100)
    description = models.TextField(_("درباره اثر"))
    

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Work_detail", kwargs={"pk": self.pk})
