import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


POEM = _('شعر')
STORY = _('داستان')
SC = _('فیلمنامه')
PI = _('نمایشنامه')
PAINTING = _('نقاشی')
WRITING = _('خوش‌نویسی')
DESIGN = _('طراحی')
MUSIC = _('موسیقی')
SC = _('سورس کد')
DA = _('هنر دیجیتال')
DC = _('محتوای دیجیتال')
OTHER = _('سایر')
WORK_TYPE = [
    (POEM, _('شعر')),
    (STORY, _('داستان')),
    (SC, _('فیلمنامه')),
    (PI, _('نمایشنامه')),
    (PAINTING, _('نقاشی')),
    (WRITING, _('خوش‌نویسی')),
    (DESIGN, _('طراحی')),
    (MUSIC, _('موسیقی')),
    (SC, _('سورس کد')),
    (DA, _('هنر دیجیتال')),
    (DC, _('محتوای دیجیتال')),
    (OTHER, _('سایر')),
]

# Create your models here.
class Work(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("عنوان"), max_length=100)
    work_type= models.CharField(_("نوع اثر"), max_length=100, choices=WORK_TYPE)
    description = models.TextField(_("درباره اثر"), blank=True, null=True)
    work_image = models.ImageField(_("تصویر شاخص اثر"), upload_to='work_images/')
    

    class Meta:
        verbose_name = _("Work")
        verbose_name_plural = _("Works")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("work-detail", kwargs={"uuid": self.uuid})

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
        return reverse("work-image-detail", kwargs={"uuid": self.uuid})