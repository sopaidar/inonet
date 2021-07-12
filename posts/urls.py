from django.urls import path

from .views import (
    PostCreateView,
    Timeline,
    UserLikes,
    LikeCreateView,
    DisLikeUpdateView
)


urlpatterns = [
    path("new/", PostCreateView.as_view(), name="new-post"),
    path("", view=Timeline.as_view(), name="timeline"),
    path("user_likes/", UserLikes.as_view(), name="user-likes"),
    path("like/<int:pk>/", LikeCreateView.as_view(), name="like"),
    path("dislike/<int:pk>/", DisLikeUpdateView.as_view(), name="dislike"),
]