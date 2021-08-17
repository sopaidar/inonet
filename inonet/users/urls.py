from django.urls import path

from inonet.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserPosts,
    UserAvatarUpdateView
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("~upload_avatar/", view=UserAvatarUpdateView.as_view(), name="user-avatar"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("<str:username>/posts/", view=UserPosts.as_view(), name="user-posts"),
]
