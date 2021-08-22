from django.urls import path

from .views import (
    UserReportCreateView,
    PostReportCreateView,
    CommentReportCreateView,
    WorkReportCreateView
)


urlpatterns = [
    path("user/<str:username>/", view=UserReportCreateView.as_view(), name="report_user"),
    path("post/<uuid:uuid>/", view=PostReportCreateView.as_view(), name="report_post"),
    path("comment/<uuid:uuid>/", view=CommentReportCreateView.as_view(), name="report_comment"),
    path("work/<uuid:uuid>/", view=WorkReportCreateView.as_view(), name="report_work"),
]