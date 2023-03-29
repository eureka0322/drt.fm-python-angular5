# -*- coding: utf-8 -*-
from django.views.generic.base import RedirectView
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.contrib import admin

from rest_framework import routers
from main.views import index, about, card, test_import, test_duration_import
from post.views import PostViewSet, CategoryViewSet
from main.sitemaps import StaticViewSitemap, DrtSitemap
from main.feed import PostFeed
admin.autodiscover()

sitemaps = {
    'pages': StaticViewSitemap(),
    'posts': DrtSitemap()
}

# Define routers
router = routers.DefaultRouter()
router.register(r'post', PostViewSet)
router.register(r'category', CategoryViewSet)

favicon_view = RedirectView.as_view(url='/static/favicon.ico', permanent=True)

urlpatterns = patterns(
    '',
    # Root URL
    url(r'^$', index, name='index'),
    url(r'^about', about, name='about'),
    url(r'^s3direct/uploads/', include('s3direct.urls')),
    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots.txt', include('robots.urls')),
    url(r'^feed', PostFeed()),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^import', test_import, name='test-import'),
    url(r'^duration', test_duration_import, name='test-duration'),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^favicon\.ico', favicon_view, name='favicon'),
    url(r'^\D+\d+|\D|\d?$', card, name='base-card'),
    # url(r'^api/auth/', include('authentication.urls')),
)
