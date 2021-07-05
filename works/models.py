from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Work(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    title = models.CharField(_("عنوان"), max_length=100)
    work_type= models.CharField(_("نوع اثر"), max_length=100)
    description = models.TextField(_("درباره اثر"), blank=True, null=True)
    work_image = models.ImageField(_("تصویر شاخص اثر"), upload_to='work_images/')
    

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Work_detail", kwargs={"pk": self.pk})

class WorkImages(models.Model):

    title = models.CharField(_("عنوان"), max_length=100)
    work_type= models.CharField(_("نوع اثر"), max_length=100)
    description = models.TextField(_("درباره اثر"), blank=True, null=True)
    

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Work_detail", kwargs={"pk": self.pk})