from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateViewGreenPoint, DetailsViewGreenPoint, CreateViewBadge, DetailsViewBadge, CreateViewStats,DetailsViewStats, CreateViewUserProfile, DetailsViewUserProfile

urlpatterns = {
    url(r'^greenpoint/$', CreateViewGreenPoint.as_view(), name="createGreenPoint"),
    url(r'^greenpoint/(?P<pk>[0-9]+)/$', DetailsViewGreenPoint.as_view(), name="detailsGreenPoint"),
    url(r'^badge/$', CreateViewBadge.as_view(), name="createBadge"),
    url(r'^badge/(?P<pk>[0-9]+)/$', DetailsViewBadge.as_view(), name="detailsBadge"),
    url(r'^userProfile/$', CreateViewUserProfile.as_view(), name="createUser"),
    url(r'^userProfile/(?P<pk>[0-9]+)/$', DetailsViewUserProfile.as_view(), name="detailsUser"),
    url(r'^stats/$', CreateViewStats.as_view(), name="createStats"),
    url(r'^stats/(?P<pk>[0-9]+)/$', DetailsViewStats.as_view(), name="detailsStats"),
}

urlpatterns = format_suffix_patterns(urlpatterns)