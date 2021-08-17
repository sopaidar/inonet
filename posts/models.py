import uuid
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import BLANK_CHOICE_DASH
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

NW = _("اثر جدید")
NF = _("گواهی زمانی جدید")
NP = _("خبر جدید")
SP = _("خبر بازنشر شده")
POST_TYPES = [
    (NW, _("اثر جدید")),
    (NF, _("گواهی زمانی جدید")),
    (NP, _("خبر جدید")),
    (SP, _("خبر بازنشر شده"))
]

# Create your models here.
class Post(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    work = models.ForeignKey("works.Work", verbose_name=_("اثر"), on_delete=models.CASCADE, null=True, blank=True)
    shared_post = models.ForeignKey("self", verbose_name=_("خبر بازنشر شده"), on_delete=models.CASCADE, blank=True, null=True)
    fingerprint = models.ForeignKey("fingerprints.Fingerprint", verbose_name=_("اثر"), on_delete=models.CASCADE, null=True, blank=True)
    post_type = models.CharField(_("نوع پست"), choices=POST_TYPES, max_length=50)
    text = models.TextField(_("متن پست"), max_length=511)
    image = models.ImageField(_("تصویر"), upload_to='posts/', blank=True, null=True)
    draft = models.BooleanField(_("پیش‌نویس"), default=False, null=False, blank=False)
    likes = models.IntegerField(_("تعداد لایک‌ها"), default=0)
    comments = models.IntegerField(_("تعداد نظرها"), default=0)
    shares = models.IntegerField(_("تعداد به اشتراک گذاری‌ها"), default=0)


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return f"post: {self.uuid}- user:{self.user.username}"

    def get_absolute_url(self):
        return reverse("Post_detail", kwargs={"uuid":self.uuid})

class Like(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, verbose_name=_("پست"), on_delete=models.CASCADE)
    liked = models.BooleanField(_("لایک شده"), default=True)
    date_time = models.DateTimeField(_("زمان"),auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_like"),
        ]
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")

    def __str__(self):
        return f"post: {self.post.uuid} - username: {self.user.username}"

    def get_absolute_url(self):
        return reverse("Like_detail", kwargs={"uuid":self.uuid})

class Comment(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, verbose_name=_("پست"), on_delete=models.CASCADE)
    text = models.TextField(_("متن کامنت"), max_length=255, blank=False, null=False)
    answered_to = models.ForeignKey("self", verbose_name=_("کامنت پاسخ داده شده"), on_delete=models.CASCADE, blank=True, null=True, default= None)
    posted = models.BooleanField(_("بازنشر شده"), default=True)
    date_time = models.DateTimeField(_("زمان"),auto_now=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"post: {self.post.uuid} - username: {self.user.username}"

    def get_absolute_url(self):
        return reverse("Comment_detail", kwargs={"uuid":self.uuid})



class Share(models.Model):

    user = models.ForeignKey("users.User", verbose_name=_("کاربر"), on_delete=models.CASCADE)
    uuid = models.UUIDField(_("uuid"), unique=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, verbose_name=_("پست"), on_delete=models.CASCADE)
    shared = models.BooleanField(_("بازنشر شده"), default=True)
    date_time = models.DateTimeField(_("زمان"),auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_shares"),
        ]
        verbose_name = _("Share")
        verbose_name_plural = _("Shares")

    def __str__(self):
        return f"post: {self.post.uuididid} - username: {self.user.username}"

    def get_absolute_url(self):
        return reverse("Share_detail", kwargs={"uuid":self.uuid})

