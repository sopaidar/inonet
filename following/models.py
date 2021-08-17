from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Follow(models.Model):

    follower = models.ForeignKey("users.User", verbose_name=_("کاربر فالوکننده"), on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey("users.User", verbose_name=_("کاربر فالوشونده"), on_delete=models.CASCADE, related_name="followed")
    date_time = models.DateTimeField(_("زمان"), auto_now=True)
    following_status = models.BooleanField(_("فالو شده"), default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followed'], name="unique_follow"),
        ]
        verbose_name = _("Follw")
        verbose_name_plural = _("Follws")

    def __str__(self):
        return self.follower

    # def get_absolute_url(self):
    #     return reverse("Follw_detail", kwargs={"uuid": self.uuid})

