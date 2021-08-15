from django.urls import path

from .views import (
    UserFollowings,
    FollowCreateView,
    UnfolowUpdateView
)


urlpatterns = [
    path("user_followings/", UserFollowings.as_view(), name="user_followings"),
    path("<str:username>/follow/", FollowCreateView.as_view(), name="follow"),
    path("<str:username>/unfollow/", UnfolowUpdateView.as_view(), name="unfollow"),
]
