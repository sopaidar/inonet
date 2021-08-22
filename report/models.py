import uuid
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
POST = _("پست")
USER = _("کاربر")
COMMENT = _("نظر")
WORK = _("اثر")
REPORT_TYPE_CHOICES = [
    (POST, _("پست")),
    (USER, _("کاربر")),
    (COMMENT, _("نظر")),
    (WORK, _("اثر")),
]

DL = _("از این مورد خوشم نمی‌آید")
NM = _("محتوای غیراخلاقی")
HS = _("نفرت پراکنی نسبت به قومیت، زبان، ملیت یا گروهی خاص")
DI = _("اطلاعات نادرست")
BT = _("آزار یا تهدید")
SF = _("کلاه‌برداری یا تقلب")
IP = _("نقض حقوق مالکیت فکری")
SS = _("تبلیغ خودکشی یا آزار رساندن به خود")
OI = _("دیگر موارد غیرقانونی")

REPORT_SUBJECT_CHOICES = [
    (DL, _("از این مورد خوشم نمی‌آید")),
    (NM, _("محتوای غیراخلاقی")),
    (HS, _("نفرت پراکنی نسبت به قومیت، زبان، ملیت یا گروهی خاص")),
    (DI, _("اطلاعات نادرست")),
    (BT, _("آزار یا تهدید")),
    (SF, _("کلاه‌برداری یا تقلب")),
    (IP, _("نقض حقوق مالکیت فکری")),
    (SS, _("تبلیغ خودکشی یا آزار رساندن به خود")),
    (OI, _("دیگر موارد غیرقانونی")),
]

class Report(models.Model):

    reporter = models.ForeignKey("users.User", verbose_name=_("گزارش کننده"), on_delete=models.CASCADE, null=True, blank=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    report_type = models.CharField(_("نوع گزارش"), max_length=50, choices=REPORT_TYPE_CHOICES)
    report_subject = models.CharField(_("موضوع گزارش"), max_length=50, choices=REPORT_SUBJECT_CHOICES)
    post = models.ForeignKey("posts.Post", verbose_name=_("پست گزارش شده"), on_delete=models.CASCADE, null=True, blank=True, related_name="report_post")    
    user = models.ForeignKey("users.User", verbose_name=_("کاربر  گزارش شده"), on_delete=models.CASCADE, null=True, blank=True, related_name="report_user")
    comment = models.ForeignKey("posts.Comment", verbose_name=_("نظر  گزارش شده"), on_delete=models.CASCADE, null=True, blank=True, related_name="report_comment")  
    work = models.ForeignKey("works.Work", verbose_name=_("اثر  گزارش شده"), on_delete=models.CASCADE, null=True, blank=True, related_name="report_work")
    date_time_reported = models.DateTimeField(_("تاریخ و زمان گزارش"), auto_now=True)
    description = models.TextField(_("شرح"), blank=True, null=True)
    seen = models.BooleanField(_("دیده شده"), default=False)
    date_time_checked = models.DateTimeField(_("زمان اتمام بررسی"), auto_now=False, null=True, blank=True)
    checked = models.BooleanField(_("بررسی شده"), default=False)
    result = models.TextField(_("نتیجه"), blank=True, null=True)

    class Meta:
        verbose_name = _("Reort")
        verbose_name_plural = _("Reorts")

    def __str__(self):
        return self.report_type

    def get_absolute_url(self):
        return reverse("Reort_detail", kwargs={"pk": self.pk})
