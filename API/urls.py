from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateViewGreenPoint, DetailsViewGreenPoint, CreateViewBadge, DetailsViewBadge, CreateViewStats,\
    DetailsViewStats, CreateViewUserProfile, DetailsViewUserProfile, CreateViewUser, DetailsViewUser, ObtainAuthToken, \
    GameReportView, RedPointView, UserGameReportView, UserReport

urlpatterns = {
    url(r'^greenpoint/$', CreateViewGreenPoint.as_view(), name="createGreenPoint"),
    url(r'^greenpoint/(?P<pk>[0-9]+)/$', DetailsViewGreenPoint.as_view(), name="detailsGreenPoint"),
    url(r'^badge/$', CreateViewBadge.as_view(), name="createBadge"),
    url(r'^badge/(?P<pk>[a-zA-Z]+)/$', DetailsViewBadge.as_view(), name="detailsBadge"),
    url(r'^user/$', CreateViewUser.as_view(), name="createUser"),
    url(r'^user/(?P<pk>[0-9]+)/$', DetailsViewUser.as_view(), name="detailsUser"),
    url(r'^profile/$', CreateViewUserProfile.as_view(), name="createUserProfile"),
    url(r'^profile/(?P<pk>[0-9]+)/$', DetailsViewUserProfile.as_view(), name="detailsUserProfile"),
    url(r'^stats/$', CreateViewStats.as_view(), name="createStats"),
    url(r'^stats/(?P<pk>[a-zA-Z]+)/$', DetailsViewStats.as_view(), name="detailsStats"),
    url(r'^api-token-auth/', ObtainAuthToken.as_view(),name="login"),
    url(r'^game/$', GameReportView.as_view(), name="game"),
    url(r'^game/(?P<user>[0-9]+)/$', UserGameReportView.as_view(), name="userGame"),
    url(r'^redpoint/$', RedPointView.as_view(), name="redpoint"),
    url(r'^report/(?P<user>[0-9]+)/$', UserReport.as_view(), name="report"),
}

urlpatterns = format_suffix_patterns(urlpatterns)