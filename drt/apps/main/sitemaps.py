from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from post.models import Post


class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 1

    def items(self):
        return ['index', 'about']

    def location(self, item):
        return reverse(item)


class DrtSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.2

    def items(self):
        return Post.objects.all()

    def location(self, item):
        return '/' + item.slug
        # reverse('base-card', kwargs={'slug': item.slug})
