# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = {
    url(r'^treepoint/$', CreateViewTreePoint.as_view(), name="createTreePoint"),
    url(r'^treepoint/(?P<pk>[0-9]+)/$', DetailsViewTreePoint.as_view(), name="detailsTreePoint"),
    url(r'^badge/$', CreateViewBadge.as_view(), name="createBadge"),
    url(r'^badge/(?P<pk>[a-zA-Z]+)/$', DetailsViewBadge.as_view(), name="detailsBadge"),
    url(r'^user/$', CreateViewUser.as_view(), name="createUser"),
    url(r'^user/(?P<pk>[0-9]+)/$', DetailsViewUser.as_view(), name="detailsUser"),
    url(r'^profile/$', CreateViewUserProfile.as_view(), name="createUserProfile"),
    url(r'^profile/(?P<pk>[0-9]+)/$', DetailsViewUserProfile.as_view(), name="detailsUserProfile"),
    url(r'^stats/$', CreateViewStats.as_view(), name="createStats"),
    url(r'^stats/(?P<pk>[a-zA-Z]+)/$', DetailsViewStats.as_view(), name="detailsStats"),
    url(r'^city/$', CityStatsView.as_view(), name="cityquery"),
    url(r'^api-token-auth/', ObtainAuthToken.as_view(),name="login"),
    url(r'^game/$', GameReportView.as_view(), name="game"),
    url(r'^game/(?P<user>[0-9]+)/$', UserGameReportView.as_view(), name="userGame"),
    url(r'^report/(?P<user>[0-9]+)/$', UserReport.as_view(), name="report"),
    url(r'^reset/password_reset$',ResetPasswordView.as_view(), name="password_reset"),
    url(r'^reset/(?P<token>.+)$',Password_Reset_Confirm.as_view(),name='password_reset_confirm')
}

urlpatterns = format_suffix_patterns(urlpatterns)