from django.urls import path

from .views import (
    PostCreateView,
    SharePostCreateView,
    Timeline,
    UserLikes,
    LikeCreateView,
    DisLikeUpdateView,
    ShareCreateView,
    UnShareUpdateView,
    CommentCreateView,
    PostComments,
    PostDetailView
)


urlpatterns = [
    path("new/", PostCreateView.as_view(), name="new-post"),
    path("new/<uuid:uuid>/", SharePostCreateView.as_view(), name="new-share-post"),
    path("", view=Timeline.as_view(), name="timeline"),
    path("user_likes/", UserLikes.as_view(), name="user-likes"),
    path("like/<uuid:uuid>/", LikeCreateView.as_view(), name="like"),
    path("dislike/<uuid:uuid>/", DisLikeUpdateView.as_view(), name="dislike"),
    path("share/<uuid:uuid>/", ShareCreateView.as_view(), name="share"),
    path("unshare/<uuid:uuid>/", UnShareUpdateView.as_view(), name="unshare"),
    path("<uuid:uuid>/comments/new/", CommentCreateView.as_view(), name="new-comment"),
    path("<uuid:uuid>/comments/", PostComments.as_view(), name="post-comments"),
    path("<uuid:uuid>/", PostDetailView.as_view(), name="post-detail"),

]
