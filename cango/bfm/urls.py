from django.conf.urls import url
from django.contrib import admin
from .views import *
urlpatterns = [
    url(r'^user/$', UserInfoUpdateView.as_view()),
    url(r'^user/rank/$', UserRankList.as_view()),
    url(r'^user/place/$', UserPlaceList.as_view()),
    url(r'^search/$', SearchPlace.as_view()),
    url(r'^place/$', PlaceView.as_view()),
    url(r'^place/comment/$', CommentView.as_view()),
    url(r'^place/like/$', LikeView.as_view()),
    url(r'^bookmark/$', BookmarkView.as_view()),
    url(r'^verify/$', VerifyView.as_view(), name='verify_main'),
    url(r'^verify/(?P<pk>[0-9]+)/$', DetailView.as_view(), name='verify_detail'),
    url(r'^verify/fail/$', FailView.as_view(), name='fail'),
    url(r'^verify/confirm/$', VerifyConfirmView.as_view(), name='verify_confirm'),
]