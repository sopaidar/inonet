from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, ListView
from posts.models import Post

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "bio"]
    success_message = _("حساب کاربری با موفقیت به روزرسانی شد!")

    def form_valid(self, form):
        form.instance.name = f'{form.cleaned_data.get("first_name")} {form.cleaned_data.get("last_name")}'
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.user.get_absolute_url()  # type: ignore [union-attr]

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class UserPosts(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 20
    template_name = "posts/list.html"
    def get_queryset(self, **kwargs):
        user = User.objects.get(username=self.kwargs["username"])
        qs = Post.objects.filter(user=user,draft=False).order_by("-pk")
        return qs


class UserAvatarUpdateView(LoginRequiredMixin, UpdateView):
    model= User
    fields= ["avatar"]
    template_name = "works/detail.html"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return JsonResponse({'msg': 'success', 'new_pic_url': self.object.avatar.url})

    def form_invalid(self, form):
        return JsonResponse({'msg': 'failed', 'errors': form._errors})
