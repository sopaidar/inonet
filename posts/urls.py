from django.urls import path

from .views import (
    PostCreateView,
    Timeline,
    UserLikes,
    LikeCreateView,
    DisLikeUpdateView,
    ShareCreateView,
    UnShareUpdateView,
    CommentCreateView,
    PostComments
)


urlpatterns = [
    path("new/", PostCreateView.as_view(), name="new-post"),
    path("", view=Timeline.as_view(), name="timeline"),
    path("user_likes/", UserLikes.as_view(), name="user-likes"),
    path("like/<int:pk>/", LikeCreateView.as_view(), name="like"),
    path("dislike/<int:pk>/", DisLikeUpdateView.as_view(), name="dislike"),
    path("share/<int:pk>/", ShareCreateView.as_view(), name="share"),
    path("unshare/<int:pk>/", UnShareUpdateView.as_view(), name="unshare"),
    path("<int:pk>/comments/new/", CommentCreateView.as_view(), name="new-comment"),
    path("<int:pk>/comments/", PostComments.as_view(), name="post-comments"),

]
