from django.db import models
from django.contrib.sites.models import Site
from s3direct.fields import S3DirectField


class PodcastFeed(models.Model):
    EXPLICIT_CHOICES = (
        (False, u'No'),
        (True, u'Yes'),
    )
    site = models.OneToOneField(Site)
    title = models.CharField("Title", max_length=255, default=u'Dorm Room Tycoon - Business, Design &amp; Technology Interviews')
    description = models.TextField("Description", default=u'The podcast show that interviews the biggest names in business, design and tech.')
    image = S3DirectField("Image URL", dest='image', default=u'')
    subtitle = models.TextField("iTunes Subtitle", default=u'Insightful interviews for hackers, product designers and startup founders. Learning from the world\'s most influential creators!')
    author = models.CharField("iTunes Owner Name", max_length=255, default=u'William Channer')
    email = models.CharField("iTunes Owner Email", max_length=255, default=u'william.channer@gmail.com')
    explicit = models.BooleanField("iTunes Explicit", max_length=1, choices=EXPLICIT_CHOICES, default=True)
    summary = models.TextField("iTunes Summary", default=u'Interviews for designers, hackers, and startup founders.')
    keywords = models.TextField("iTunes Keywords", default=u'drt, design, marketing, business, entrepreneurship, silicon valley, kickstarter, product, innovation, startup, product hunt')
    copyright = models.CharField("Copyright", max_length=255, default=u'Copyright %s Dorm Room Tycoon')
