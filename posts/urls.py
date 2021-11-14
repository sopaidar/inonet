from django.urls import path

from .views import (
    PostCreateView,
    SharePostCreateView,
    Timeline,
    UserLikes,
    UserCommentLikes,
    LikeCreateView,
    DisLikeUpdateView,
    ShareCreateView,
    UnShareUpdateView,
    CommentCreateView,
    PostComments,
    PostDetailView,
    CommentLikeCreateView,
    CommentDisLikeUpdateView,
    WorkTimeline
)


urlpatterns = [
    path("new/", PostCreateView.as_view(), name="new-post"),
    path("new/<uuid:uuid>/", SharePostCreateView.as_view(), name="new-share-post"),
    path("", view=Timeline.as_view(), name="timeline"),
    path("user_likes/", UserLikes.as_view(), name="user-likes"),
    path("user_comment_likes/", UserCommentLikes.as_view(), name="user_comment_likes"),
    path("like/<uuid:uuid>/", LikeCreateView.as_view(), name="like"),
    path("dislike/<uuid:uuid>/", DisLikeUpdateView.as_view(), name="dislike"),
    path("share/<uuid:uuid>/", ShareCreateView.as_view(), name="share"),
    path("unshare/<uuid:uuid>/", UnShareUpdateView.as_view(), name="unshare"),
    path("<uuid:uuid>/comments/new/", CommentCreateView.as_view(), name="new-comment"),
    path("<uuid:uuid>/comments/", PostComments.as_view(), name="post-comments"),
    path("<uuid:uuid>/", PostDetailView.as_view(), name="post-detail"),
    path("like_comment/<uuid:uuid>/", CommentLikeCreateView.as_view(), name="comment_like"),
    path("dislike_comment/<uuid:uuid>/", CommentDisLikeUpdateView.as_view(), name="comment_dislike"),
    path("work_posts/<uuid:uuid>/", view=WorkTimeline.as_view(), name="work_timeline"),
]
